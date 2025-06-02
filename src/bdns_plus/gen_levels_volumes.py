"""simple functions to generate levels and volumes configurations."""

# from .models import _Base

# MODEL_FIELDS = list(_Base.__pydantic_fields__.keys())
MODEL_FIELDS = ["id", "code", "name"]
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


def gen_levels_config(*, level_min: int = LEVEL_MIN, level_max: int = LEVEL_MAX) -> list[list]:
    map_code_id = gen_levels(low=level_min, high=level_max)
    map_code_name = {level: gen_level_name(level) for level in map_code_id.keys()}
    header = MODEL_FIELDS
    rows = [[map_code_id[x], x, map_code_name[x]] for x in map_code_id.keys()]
    return [header, *rows]


def gen_volumes_config(*, no_volumes: int = NO_VOLUMES) -> list[list]:
    header = MODEL_FIELDS
    rows = [[n, n, f"Volume {n}"] for n in range(1, no_volumes + 1)]
    return [header, *rows]
