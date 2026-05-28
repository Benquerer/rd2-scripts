# =============================================================
# main.py  - only service that touches routers
# Run:  uvicorn main:app --host 0.0.0.0 --port 8000
# =============================================================
import asyncio
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import inventory
import config_store
from ssh_service import GroupSession, test_reachable, _open

app = FastAPI(title="BGP Lab API")

# sllow cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# request models
class Creds(BaseModel):
    username: str
    password: str
    secret: str | None = None


class ConfigReq(BaseModel):
    group: str
    router: str
    creds: Creds
    commands: list[str] | None = None   # None = use default-config


class EraseReq(BaseModel):
    group: str
    router: str
    creds: Creds


class VerifyReq(BaseModel):
    group: str
    creds: Creds


# inventory (no ssh)

@app.get("/api/groups")
def groups():
    out = []
    for g in inventory.list_groups():
        out.append({"group": g, "routers": inventory.routers_for(g)})
    return out


@app.get("/api/default-config")
def default_config(group: str, router: str):
    return {"text": config_store.raw_text(group, router)}


# helpers

def _creds_dict(c: Creds):
    return {
        "username": c.username,
        "password": c.password,
        "secret": c.secret or c.password,
    }


def _do_configure(req: ConfigReq):
    """Blocking. Returns a list of {level,message} events."""
    events = []
    cmds = req.commands
    if cmds is None:
        cmds = config_store.load_router(req.group, req.router)
        if not cmds:
            return [{"level": "error",
                     "message": f"No default config for {req.group}-{req.router}"}]
    with GroupSession(req.group, _creds_dict(req.creds)) as s:
        for lvl, msg in s.connect(req.router):
            events.append({"level": lvl, "message": msg})
        if req.router.upper() in s.conns:
            for lvl, msg in s.send_config(req.router, cmds):
                events.append({"level": lvl, "message": msg})
    return events


def _do_erase(req: EraseReq):
    events = []
    with GroupSession(req.group, _creds_dict(req.creds)) as s:
        for lvl, msg in s.connect(req.router):
            events.append({"level": lvl, "message": msg})
        if req.router.upper() in s.conns:
            for lvl, msg in s.erase(req.router):
                events.append({"level": lvl, "message": msg})
    return events


def _do_verify(req: VerifyReq):
    events = []
    group = req.group.upper()
    with GroupSession(group, _creds_dict(req.creds)) as s:
        for router in inventory.routers_for(group):
            for lvl, msg in s.connect(router):
                events.append({"level": lvl, "message": msg})
            if router not in s.conns:
                continue
            ospf = s.run(router, "show ip ospf neighbor")
            full = sum(1 for l in ospf.splitlines() if "FULL" in l)
            events.append({
                "level": "ok" if full else "warn",
                "message": f"{router}: OSPF {full} FULL",
            })
            bgp = s.run(router, "show ip bgp summary")
            up = sum(1 for l in bgp.splitlines()
                     for p in [l.split()] if len(p) >= 9 and p[-1].isdigit())
            events.append({
                "level": "ok" if up else "warn",
                "message": f"{router}: BGP {up} established",
            })
    return events


# action endpoints

@app.post("/api/configure")
async def configure(req: ConfigReq):
    if not inventory.is_valid(req.group, req.router):
        return {"events": [{"level": "error", "message": "Invalid group/router"}]}
    events = await asyncio.to_thread(_do_configure, req)
    return {"events": events}


@app.post("/api/erase")
async def erase(req: EraseReq):
    if not inventory.is_valid(req.group, req.router):
        return {"events": [{"level": "error", "message": "Invalid group/router"}]}
    events = await asyncio.to_thread(_do_erase, req)
    return {"events": events}


@app.post("/api/verify")
async def verify(req: VerifyReq):
    if not inventory.is_valid(req.group):
        return {"events": [{"level": "error", "message": "Invalid group"}]}
    events = await asyncio.to_thread(_do_verify, req)
    return {"events": events}


@app.post("/api/test")
async def test(req: VerifyReq):
    """Reachability test for every router in a group (with tunnels)."""
    results = []

    def work():
        out = []
        with GroupSession(req.group.upper(), _creds_dict(req.creds)) as s:
            for router in inventory.routers_for(req.group.upper()):
                for lvl, msg in s.connect(router):
                    out.append({"level": lvl, "message": msg})
        return out

    results = await asyncio.to_thread(work)
    return {"events": results}


# websocket terminal

@app.websocket("/ws/terminal")
async def terminal(ws: WebSocket):
    """
    Browser sends an opening JSON {host, username, password, secret}.
    After that, each text frame is a command line; output is streamed
    back. Direct connection only (single arbitrary IP).
    """
    await ws.accept()
    conn = None
    try:
        first = await ws.receive_text()
        cfg = json.loads(first)
        creds = {
            "username": cfg["username"],
            "password": cfg["password"],
            "secret": cfg.get("secret") or cfg["password"],
        }
        host = cfg["host"]

        def open_conn():
            return _open(host, creds)

        try:
            conn = await asyncio.to_thread(open_conn)
        except Exception as e:
            await ws.send_text(f"[connection failed] {e}")
            await ws.close()
            return

        await ws.send_text(f"[connected to {host}]\n")

        while True:
            line = await ws.receive_text()
            cmd = line.strip()
            if cmd in ("exit", "quit"):
                break

            def run():
                # config-ish commands need config mode; everything
                # else is treated as an exec/show command.
                return conn.send_command_timing(
                    cmd, strip_prompt=False, strip_command=False
                )

            try:
                out = await asyncio.to_thread(run)
            except Exception as e:
                out = f"[error] {e}"
            await ws.send_text(out)

    except WebSocketDisconnect:
        pass
    finally:
        if conn is not None:
            try:
                await asyncio.to_thread(conn.disconnect)
            except Exception:
                pass
