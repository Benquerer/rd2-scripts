import os
import re

BASE = os.path.join(os.path.dirname(__file__), "..", "default-configs")
_MARKER = re.compile(r"^!\s*=+\s*(\S+)\s*=+\s*$")


def _path(group):
    return os.path.join(BASE, f"{group.lower()}.cfg")


def load_group(group):
    """
    Return {router_name: [command, ...]} parsed from the group's .cfg.
    Lines before the first marker and blank/comment lines are dropped.
    """
    path = _path(group)
    if not os.path.exists(path):
        return {}

    sections = {}
    current = None
    with open(path) as f:
        for raw in f:
            line = raw.rstrip("\n")
            m = _MARKER.match(line.strip())
            if m:
                current = m.group(1).upper()
                sections[current] = []
                continue
            if current is None:
                continue
            if not line.strip() or line.strip().startswith("!"):
                continue
            sections[current].append(line)
    return sections


def load_router(group, router):
    """Return the command list for one router, or [] if absent."""
    return load_group(group).get(router.upper(), [])


def raw_text(group, router=None):
    """Return raw .cfg text (whole group, or one router's section)."""
    path = _path(group)
    if not os.path.exists(path):
        return ""
    if router is None:
        with open(path) as f:
            return f.read()
    cmds = load_router(group, router)
    return "\n".join(cmds)
