"""
default configuration for bdns_plus is as follows:

- level ground and above are 2-digit zero-padded integers up to a max of 89
- level basement 1 and below are 2-digit integers 99 - 90
- the volume is a single digit integer 1 - 9
"""
from frictionless import Package, Resource, describe
from frictionless.resources import TableResource
LEVEL_DIGITS = 2
LEVEL_MIN, LEVEL_MAX, BASEMENT_1 = -10, 89, 10**LEVEL_DIGITS - 1
VOLUME = 1

def get_level_id(level: int) -> int:
    if level < 0:
        return BASEMENT_1 + 1 + level
    else:
        return level

def gen_levels(low=LEVEL_MIN, high=LEVEL_MAX):
    return {n: get_level_id(n) for n in range(low, high + 1)}

def gen_level_name(level: int) -> str:
    if level == 0:
        return "Ground"
    elif level < 0:
        return f"Basement {-level}"
    else:
        return f"Level {level}"

def gen_levels_config():
    map_level_id = gen_levels()
    map_level_name = {level: gen_level_name(level) for level in map_level_id.keys()}
    header = ['level', 'level_id', 'level_name']
    rows = [[x, map_level_id[x], map_level_name[x]] for x in map_level_id.keys()]
    data = [header] + rows
    return data

def gen_volumes_config():
    header = ['volume', 'volume_id', 'volume_name']
    rows = [[n, n, f"Volume {n}"] for n in range(1, 10)]
    data = [header] + rows
    return data

def gen_levels_resource():
    data= gen_levels_config()
    res = TableResource(name="levels", data=data)
    res.read_rows()
    return res

def gen_volumes_resource():
    data= gen_volumes_config()
    res = TableResource(name="volumes", data=data)
    res.read_rows()
    return res

def gen_config_package():
    res_levels = gen_levels_resource()
    res_volumes = gen_volumes_resource()

    pkg = Package(
        name='bdns-plus',
        resources=[res_levels, res_volumes]
    )
    return pkg
