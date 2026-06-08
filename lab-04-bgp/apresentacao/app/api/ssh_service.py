# =============================================================
# ssh_service.py - SSH/netmiko usage
# =============================================================
from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

from inventory import ROUTERS, CONFIG_ORDER, JUMP_HOSTS


def _device(host, creds, sock=None):
    d = {
        "device_type": "cisco_ios",
        "host": host,
        "username": creds["username"],
        "password": creds["password"],
        "secret": creds.get("secret", creds["password"]),
        "timeout": 15,
        "fast_cli": False,
    }
    if sock is not None:
        d["sock"] = sock
    return d


def _open(host, creds, jump_chain=None):
    """
    Open a single SSH connection, optionally tunneled through the
    last connection in jump_chain (a direct-tcpip channel).
    Raises on failure so the caller can report a clean message.
    """
    sock = None
    if jump_chain:
        sock = jump_chain[-1].remote_conn.transport.open_channel(
            "direct-tcpip", (host, 22), ("", 0)
        )
    conn = ConnectHandler(**_device(host, creds, sock=sock))
    conn.enable()
    return conn


class GroupSession:
    """
    Holds open connections to a group's routers and builds the
    jump chain needed to reach any one of them. Use as a context
    manager so everything is cleaned up.
    """

    def __init__(self, group, creds):
        self.group = group.upper()
        self.creds = creds
        self.conns = {}  # router_name -> ConnectHandler

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close_all()

    def _chain_for(self, router):
        names = JUMP_HOSTS.get(router, [])
        return [self.conns[n] for n in names if n in self.conns]

    def connect(self, router):
        """
        Ensure router (and every jump host it depends on) is connected.
        Yields (level, message) progress tuples. Returns the conn via
        self.conns[router], or leaves it absent on failure.
        """
        router = router.upper()
        for hop in JUMP_HOSTS.get(router, []):
            if hop not in self.conns:
                yield from self.connect(hop)
                if hop not in self.conns:
                    yield ("error", f"Cannot reach {router}: jump host {hop} failed")
                    return

        if router in self.conns:
            return  

        ip = ROUTERS[self.group][router]
        chain = self._chain_for(router)
        try:
            conn = _open(ip, self.creds, chain if chain else None)
            self.conns[router] = conn
            yield ("ok", f"Connected to {self.group}-{router} ({ip})")
        except NetmikoTimeoutException:
            yield ("error", f"Timeout connecting to {self.group}-{router} ({ip})")
        except NetmikoAuthenticationException:
            yield ("error", f"Auth failed for {self.group}-{router} ({ip})")
        except Exception as e:
            yield ("error", f"Error connecting to {self.group}-{router}: {e}")

    def send_config(self, router, commands):
        """Apply a list of config lines to an already-connected router."""
        router = router.upper()
        conn = self.conns.get(router)
        if not conn:
            yield ("error", f"{router} not connected")
            return
        try:
            conn.send_config_set(commands)
            conn.save_config()
            yield ("ok", f"Config applied to {self.group}-{router}")
        except Exception as e:
            yield ("error", f"Error applying config to {router}: {e}")

    def run(self, router, command):
        """Run a single show/exec command, return its output text."""
        router = router.upper()
        conn = self.conns.get(router)
        if not conn:
            return ""
        try:
            return conn.send_command(command)
        except Exception as e:
            return f"[error] {e}"

    def erase(self, router):
        """Erase startup-config and reload a router."""
        router = router.upper()
        conn = self.conns.get(router)
        if not conn:
            yield ("error", f"{router} not connected")
            return
        try:
            conn.send_command_timing(
                "erase startup-config", strip_prompt=False, strip_command=False
            )
            conn.send_command_timing("\n", strip_prompt=False, strip_command=False)
            yield ("ok", f"startup-config erased on {self.group}-{router}")
            conn.send_command_timing(
                "reload", strip_prompt=False, strip_command=False
            )
            conn.send_command_timing("\n", strip_prompt=False, strip_command=False)
            yield ("ok", f"Reload sent to {self.group}-{router}")
        except Exception as e:
            yield ("error", f"Error erasing {router}: {e}")

    def close_all(self):
        # should close farthest first
        for name in reversed(list(self.conns)):
            try:
                self.conns[name].disconnect()
            except Exception:
                pass
        self.conns.clear()


def test_reachable(host, creds):
    """Quick connect/disconnect to test a single host. Returns (ok, msg)."""
    try:
        conn = _open(host, creds)
        conn.disconnect()
        return True, f"Reachable: {host}"
    except NetmikoTimeoutException:
        return False, f"Timeout: {host}"
    except NetmikoAuthenticationException:
        return False, f"Auth failed: {host}"
    except Exception as e:
        return False, f"Error: {host}: {e}"
