# inventory.py - single group (Lab #05 Desafio, Grupo 1 / AS60101)
# The group now owns its provider routers (AS100, AS200) too, so all
# six routers are configurable through the app.

# Reachability / SSH addresses.
# R1 is the entry point on the management subnet; every other router is
# reached by tunnelling from R1 to the interface it shares with the jump
# host (directly-connected next-hop IP). The only value carried over from
# Lab 04 is R1's management address - confirm it for this lab.
ROUTERS = {
    "G1": {
        "R1":     "172.100.100.11",   # management subnet, directly reachable
        "R2":     "10.1.1.2",         # R1<->R2 link  (R2 G0/0),     via R1
        "R3":     "10.1.1.10",        # R1<->R3 serial (R3 S0/0/0),  via R1
        "R4-RIP": "10.1.1.50",        # R1<->R4 link  (R4 G0/0),     via R1
        "AS100":  "172.17.1.2",       # R1<->AS100 link (AS100 G0/0),via R1
        "AS200":  "172.21.1.2",       # R3<->AS200 link (AS200 G0/0),via R1->R3
    },
}

# group-specific data (asn used for reference; configs come from the .cfg)
GROUP_INFO = {
    "G1": {"gn": 1, "asn": 60101},
}

# configuration / display order
CONFIG_ORDER = {
    "G1": ["R1", "R2", "R3", "R4-RIP", "AS100", "AS200"],
}

# Jump chain for each router. Empty = directly reachable.
JUMP_HOSTS = {
    "R1": [],
    "R2": ["R1"],
    "R3": ["R1"],
    "R4-RIP": ["R1"],
    "AS100": ["R1"],
    "AS200": ["R1", "R3"],
}


def list_groups():
    """Return group names for the UI dropdown."""
    return list(ROUTERS)


def routers_for(group):
    """Return the ordered router names for a group."""
    return CONFIG_ORDER.get(group.upper(), [])


def is_valid(group, router=None):
    group = group.upper()
    if group not in ROUTERS:
        return False
    if router is not None and router.upper() not in ROUTERS[group]:
        return False
    return True