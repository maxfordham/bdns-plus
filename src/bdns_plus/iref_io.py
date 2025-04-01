from __future__ import annotations

import logging

from annotated_types import Annotated, Ge

logger = logging.getLogger(__name__)
level_min, level_max, ground = -9, 89, 90


def get_level_id(level: int):
    if level == 0:
        return ground
    if level < 0:
        return ground - level
    return level


def gen_levels(low, high):
    return {n: get_level_id(n) for n in range(low, high + 1)}


def serialize_iref(
    level_number: int,
    level_iref: Annotated[int, Ge(0)],
    level_min=-9,
    level_max=89,
) -> Annotated[int, Ge(0)]:
    """Return instance reference integer (>0) given a level number and level instance"""
    map_level_id = gen_levels(level_min, level_max)
    level_id = map_level_id[level_number]
    return int(f"{level_id}0{level_iref}")


def deserialize_iref(
    iref: Annotated[int, Ge(0)],
    level_min=-9,
    level_max=89,
) -> tuple[int | None, Annotated[int, Ge(0)] | None]:
    """Return a level number and level instance given a instance reference integer (>0)"""
    try:
        level_id, level_iref = str(iref).split("0", 1)
    except ValueError:
        e = f"could not split instance_reference={iref} on '0' to get level_number and level_instance_reference"
        logger.warning(e)
        return None, None
    if level_iref[0] == "0":
        level_id = level_id + "0"
    level_id, level_iref = int(level_id), int(level_iref)
    map_id_level = {v: k for k, v in gen_levels(level_min, level_max).items()}
    level_number = map_id_level[level_id]
    return level_number, level_iref


def get_next_iref(irefs: list[int], level_number: None | int = None):
    if level_number is None:
        return max(irefs) + 1
    if level_number is not None and len(irefs) == 0:
        return serialize_iref(level_number, 1)
    if level_number is not None and len(irefs) > 0:
        _ = [deserialize_iref(iref) for iref in irefs]
        level_irefs = [x[1] for x in _ if x[0] == level_number]
        if len(level_irefs) == 0:
            return serialize_iref(level_number, 1)
        return serialize_iref(level_number, max(level_irefs) + 1)
    e = f"get_next_iref error where irefs={irefs}, level_number={level_number}"
    raise ValueError(e)


def check_dict_var(data: dict, key: str):
    if key in data:
        if data[key] is not None:
            return True
    else:
        return False


def is_level_number_and_level_instance_reference(
    data: dict,
) -> None | tuple[int, int]:
    """Return values for `level_number` and `level_instance_reference`
    if they exist and are not None
    """
    if False in [
        check_dict_var(data, "level_number"),
        check_dict_var(data, "level_instance_reference"),
    ]:
        return False
    return True
