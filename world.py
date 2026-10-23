REGIONS = [
    ("Village", 1), ("Forest", 11), ("Cave", 21), ("Mountain", 31),
    ("Desert", 41), ("Ruins", 51), ("Castle", 61), ("Volcano", 71),
    ("Frozen Mountain", 81), ("Sky Temple", 90), ("Demon Realm", 100)
]

def get_current_region(level):
    active_region = "Village"
    for reg, req_lvl in REGIONS:
        if level >= req_lvl:
            active_region = reg
    return active_region