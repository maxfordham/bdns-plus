"""Instance reference integer (iref) utilities."""

from __future__ import annotations

from typing import Annotated

from annotated_types import Ge

from .models import Config, IdentifierType


def serialize_iref(  # noqa: C901, PLR0912
    level: int,
    volume_level_instance: Annotated[int, Ge(0)],
    *,
    config: Config | None = None,
    volume: int = 1,
) -> Annotated[int, Ge(0)]:
    """Return instance reference integer (>0) given a level number (+ve or -ve integer) and level instance."""
    if config is None:
        config = Config()
    level_indentifier_type = config.level_identifier_type
    volume_identifier_type = config.volume_identifier_type
    # get map_level
    if level_indentifier_type == IdentifierType.code:
        map_level = {x.code: x.id for x in config.levels}
    elif level_indentifier_type == IdentifierType.name:
        map_level = {x.name: x.id for x in config.levels}
    elif level_indentifier_type == IdentifierType.id:
        map_level = {level: level}
    else:
        e = f"level_identifier_type={level_indentifier_type} not supported"
        raise ValueError(e)

    map_level, level_lookup_key = convert_codes_type(config.levels, level, map_level)

    # get map_volume
    if volume_identifier_type == IdentifierType.code:
        map_volume = {x.code: x.id for x in config.volumes}
    elif volume_identifier_type == IdentifierType.name:
        map_volume = {x.name: x.id for x in config.volumes}
    elif volume_identifier_type == IdentifierType.id:
        map_volume = {volume: volume}
    else:
        e = f"volume_identifier_type={volume_identifier_type} not supported"
        raise ValueError(e)

    map_volume, volume_lookup_key = convert_codes_type(config.volumes, volume, map_volume)

    try:
        level_id = map_level[level_lookup_key]
    except KeyError as err:
        e = f"level={level_lookup_key} not in config.levels (length={len(config.levels)}) with identifier_type={level_indentifier_type}"
        raise ValueError(e) from err

    try:
        volume_id = map_volume[volume_lookup_key]
    except KeyError as err:
        e = f"volume={volume_lookup_key} not in config.volumes (length={len(config.volumes)}) with identifier_type={volume_identifier_type}"
        raise ValueError(e) from err

    # validator that levels and volumes are compatible
    if config.map_volume_level is not None:
        if volume_id not in config.map_volume_level:
            e = f"volume_id={volume_id} not in config.map_volume_level"
            raise ValueError(e)
        if level_id not in config.map_volume_level[volume_id]:
            e = f"level_id={level_id} not in config.map_volume_level[volume_id]"
            raise ValueError(e)

    level_id_str = str(level_id).zfill(config.level_no_digits)
    volume_id_str = str(volume_id).zfill(config.volume_no_digits)

    iref = config.iref_fstring.format(
        volume_id=volume_id_str,
        level_id=level_id_str,
        volume_level_instance=volume_level_instance,
    )
    return int(iref)


def deserialize_iref(iref: int) -> tuple[int, int]:
    """Return level number and level instance given an instance reference integer."""


def convert_codes_type(list_with_codes: list, lookup_key: str | int, mapping: dict) -> tuple[dict, str | int]:
    """Convert codes in list to strings if any code is a string."""
    types = {type(x.code) for x in list_with_codes}
    if str in types:
        return {str(k): v for k, v in mapping.items()}, str(lookup_key)
    return mapping, int(lookup_key)
