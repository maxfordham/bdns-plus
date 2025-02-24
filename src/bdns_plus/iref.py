"""Instance reference integer (iref) utilities"""

from .models import Config, IdentifierType
from typing import Annotated
from annotated_types import Ge

def serialize_iref(
    level: int,
    level_iref: Annotated[int, Ge(0)],
    config: Config | None = None,
    volume: int = 1,
    level_indentifier_type: IdentifierType = IdentifierType.number,
    volume_identifier_type: IdentifierType = IdentifierType.number,
) -> Annotated[int, Ge(0)]:
    """return instance reference integer (>0) given a level number (+ve or -ve integer) and level instance"""
    if config is None:
        config = Config()

    # get map_level
    if level_indentifier_type == IdentifierType.number:
        map_level = {x.level: x.level_id for x in config.levels}
    elif level_indentifier_type == IdentifierType.name:
        map_level = {x.level_name: x.level for x in config.levels}
    elif level_indentifier_type == IdentifierType.id:
        map_level = {level: level}
    else:
        raise ValueError(f"level_identifier_type={level_indentifier_type} not supported")

    # get map_volume
    if volume_identifier_type == IdentifierType.number:
        map_volume = {x.volume: x.volume_id for x in config.volumes}
    elif volume_identifier_type == IdentifierType.name:
        map_volume = {x.volume_name: x.volume for x in config.volumes}
    elif volume_identifier_type == IdentifierType.id:
        map_volume = {volume: volume}
    else:
        raise ValueError(f"volume_identifier_type={volume_identifier_type} not supported")

    level_id = map_level[level]
    volume_id = map_volume[volume]

    # validate that levels and volumes are compatible
    if config.map_volume_level is not None:
        if volume_id not in config.map_volume_level:
            raise ValueError(f"volume_id={volume_id} not in config.map_volume_level")
        if level_id not in config.map_volume_level[volume_id]:
            raise ValueError(f"level_id={level_id} not in config.map_volume_level[volume_id]")
        
    level_id_str = str(level_id).zfill(config.level_no_digits)
    volume_id_str = str(volume_id).zfill(config.volume_no_digits)
    
    iref = config.iref_fstring.format(volume_id=volume_id_str, level_id=level_id_str, level_instance_id=level_iref)
    return int(iref)


def deserialize_iref(iref: int) -> tuple[int, int]:
    """return level number and level instance given an instance reference integer"""
    pass
