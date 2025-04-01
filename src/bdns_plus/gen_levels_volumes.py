"""simple functions to generate levels and volumes configurations."""

LEVEL_DIGITS = 2
LEVEL_MIN, LEVEL_MAX, BASEMENT_1 = -10, 89, 10**LEVEL_DIGITS - 1
NO_VOLUMES = 9
# ^ these are the maximum values that support 2-digit zero-padded integers for levels and 1-digit integers for volumes


def get_level_id(level: int) -> int:
    if level < 0:
        return BASEMENT_1 + 1 + level
    return level


def gen_levels(*, low: int = LEVEL_MIN, high: int = LEVEL_MAX) -> dict[int, int]:
    return {n: get_level_id(n) for n in range(low, high + 1)}


def gen_level_name(level: int) -> str:
    if level == 0:
        return "Ground"
    if level < 0:
        return f"Basement {-level}"
    return f"Level {level}"


def gen_levels_config(*, level_min: int = LEVEL_MIN, level_max: int = LEVEL_MAX):
    map_level_id = gen_levels(low=level_min, high=level_max)
    map_level_name = {level: gen_level_name(level) for level in map_level_id.keys()}
    header = ["level", "level_id", "level_name"]
    rows = [[x, map_level_id[x], map_level_name[x]] for x in map_level_id.keys()]
    return [header, *rows]


def gen_volumes_config(*, no_volumes: int = NO_VOLUMES):
    header = ["volume", "volume_id", "volume_name"]
    rows = [[n, n, f"Volume {n}"] for n in range(1, no_volumes + 1)]
    return [header, *rows]
