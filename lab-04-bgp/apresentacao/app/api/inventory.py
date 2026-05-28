# Per-domain addresses
ROUTERS = {
    # groups
    "G1": {"R1": "172.100.100.11", "R3": "10.11.13.2", "R2": "10.11.23.1"},
    "G2": {"R1": "172.100.100.12", "R3": "10.12.13.2", "R2": "10.12.23.1"},
    "G3": {"R1": "172.100.100.13", "R3": "10.13.13.2", "R2": "10.13.23.1"},
    "G4": {"R1": "172.100.100.14", "R3": "10.14.13.2", "R2": "10.14.23.1"},
    "G5": {"R1": "172.100.100.15", "R3": "10.15.13.2", "R2": "10.15.23.1"},
    "G6": {"R1": "172.100.100.16", "R3": "10.16.13.2", "R2": "10.16.23.1"},
    # provider core.
    "CORE": {"AS100": "172.100.100.100", "AS200": "172.200.200.100"},
}

# group-specific data to fill config
GROUP_INFO = {
    "G1": {"gn": 11, "asn": 301},
    "G2": {"gn": 12, "asn": 302},
    "G3": {"gn": 13, "asn": 303},
    "G4": {"gn": 14, "asn": 304},
    "G5": {"gn": 15, "asn": 305},
    "G6": {"gn": 16, "asn": 306},
    "CORE": {"gn": None, "asn": None},
}

# configuration order
CONFIG_ORDER = {
    "G1": ["R1", "R3", "R2"],
    "G2": ["R1", "R3", "R2"],
    "G3": ["R1", "R3", "R2"],
    "G4": ["R1", "R3", "R2"],
    "G5": ["R1", "R3", "R2"],
    "G6": ["R1", "R3", "R2"],
    "CORE": ["AS100", "AS200"],
}

# Jump chain for each router
# Empty = directly reachable.
JUMP_HOSTS = {
    "R1": [],
    "R3": ["R1"],
    "R2": ["R1", "R3"],
    "AS100": [],
    "AS200": [],
}


def list_groups():
    """Return group names for the UI dropdown, Core last."""
    groups = [g for g in ROUTERS if g != "CORE"]
    groups.sort()
    return groups + ["CORE"]


def routers_for(group):
    """Return the ordered router names for a group."""
    group = group.upper()
    return CONFIG_ORDER.get(group, [])


def is_valid(group, router=None):
    group = group.upper()
    if group not in ROUTERS:
        return False
    if router is not None and router.upper() not in ROUTERS[group]:
        return False
    return True
