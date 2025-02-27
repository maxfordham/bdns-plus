"""data models for bdns_plus."""
from __future__ import annotations

import typing as ty
from enum import Enum

from pydantic import AliasChoices, BaseModel, Field, ImportString, model_validator

from .config import gen_levels_config, gen_volumes_config
from .default_fields import bdns_fields, instance_fields, type_fields

INSTANCE_REFERENCE_FSTRING = "{volume_id}{level_id}{level_instance_id}"


def to_records(data: list[list]) -> list[dict]:
    return [dict(zip(data[0], x)) for x in data[1:]]


# TODO: this feels a bit like repetition of pydantic... could probs use datamodel-code-gen instead...
class TagField(BaseModel):
    field_name: str
    field_aliases: list[str] = []
    allow_none: bool = False
    prefix: str = ""
    suffix: str = ""
    zfill: int | None = None
    regex: str | None = None
    validate: ImportString | None = None  # ty.Callable[[ty.Any], bool] | None = None


class TagDef(BaseModel):  # RootModel
    name: str
    description: str
    fields: list[TagField]


class ConfigType(str, Enum):
    level = "level"
    volume = "volume"
    level_instance = "level_instance"

class IdentifierType(str, Enum):
    id = "id"
    number = "number"
    name = "name"

class TagType(str, Enum):
    bdns = "bdns"
    instance = "instance"
    type = "type"

class Level(BaseModel):
    level: int
    level_id: int
    level_name: str

class Volume(BaseModel):
    volume: int
    volume_id: int
    volume_name: str

def default_levels() -> list[Level]:
    return [Level(**x) for x in to_records(gen_levels_config())]

def default_volumes() -> list[Volume]:
    return [Volume(**x) for x in to_records(gen_volumes_config())]

class Iref(BaseModel):
    level: int = Field(
        ..., validation_alias=AliasChoices("level", "level_id", "level_number", "Level", "LevelId", "LevelNumber"),
    )
    level_iref: int = Field(
        ..., validation_alias=AliasChoices("level_instance", "LevelInstance", "VolumeLevelInstance", "level_iref"),
    )
    volume: int = Field(
        1, validation_alias=AliasChoices("volume", "volume_id", "volume_number", "Volume", "VolumeId", "VolumeNumber"),
    )


class BdnsTag(TagDef):
    @model_validator(mode="before")
    @classmethod
    def _set_fields(cls, data: ty.Any) -> dict:  # noqa: ANN401
        di = {}
        di["name"] = "bdns"
        di["description"] = "TagDef Definition in accordance with Building Data Naming System"
        di["fields"] = bdns_fields(include_type=False)
        return di

class BdnsTagWithType(TagDef):
    @model_validator(mode="before")
    @classmethod
    def _set_fields(cls, data: ty.Any) -> dict:  # noqa: ANN401
        di = {}
        di["name"] = "bdns"
        di["description"] = "TagDef Definition in accordance with Building Data Naming System. Type included."
        di["fields"] = bdns_fields(include_type=True)
        return di


class TypeTag(TagDef):
    @model_validator(mode="before")
    @classmethod
    def _set_fields(cls, data: ty.Any) -> dict:  # noqa: ANN401
        di = {}
        di["name"] = "bdns"
        di["description"] = "TagDef Definition in accordance with Building Data Naming System"
        di["fields"] = type_fields()
        return di


class InstanceTag(TagDef):
    @model_validator(mode="before")
    @classmethod
    def _set_fields(cls, data: ty.Any) -> dict:  # noqa: ANN401
        di = {}
        di["name"] = "bdns"
        di["description"] = "TagDef Definition in accordance with Building Data Naming System"
        di["fields"] = instance_fields(include_type=False)
        return di

class ConfigIref(BaseModel):
    """defines params required to generate an instance ref. levels and volumes."""

    levels: list[Level] = Field(default_levels())
    volumes: list[Volume] = Field(default_volumes())
    map_volume_level: dict[int, int] | None = None  # allows for restricting volumes to known levels
    level_no_digits: int | None = None
    no_levels: int | None = None
    no_volumes: int | None = None
    volume_no_digits: int | None = None
    iref_fstring: ty.Literal["{volume_id}{level_id}{level_instance_id}"] = INSTANCE_REFERENCE_FSTRING

    @model_validator(mode="after")
    def _get_no_digits(self) -> ty.Self:
        level_ids = [len(str(x.level_id)) for x in self.levels]
        self.level_no_digits = max(level_ids)
        volume_ids = [len(str(x.volume_id)) for x in self.volumes]
        self.volume_no_digits = max(volume_ids)
        return self

    @model_validator(mode="after")
    def _get_nos(self) -> ty.Self:
        self.no_levels = len(self.levels)
        self.no_volumes = len(self.volumes)
        return self


class ConfigTags(BaseModel):
    """defines tag definitions. bdns, instance and type tags. pre-configured with sensible defaults."""

    bdns_tag: type[TagDef] = BdnsTag()
    i_tag: type[TagDef] = InstanceTag()
    t_tag: type[TagDef] = TypeTag()
    custom_i_tags: dict[str, type[TagDef]] = {}  # AbbreviationsEnum
    custom_t_tags: dict[str, type[TagDef]] = {}  # AbbreviationsEnum
    is_bdns_plus_default: bool = True

    @model_validator(mode="after")
    def _check_is_bdns_plus_default(self) -> ty.Self:

        check_default = [
            bool(isinstance(i, c))
            for i, c in zip([self.bdns_tag, self.i_tag, self.t_tag], [BdnsTag, InstanceTag, TypeTag])
        ]
        if False in check_default:
            self.is_bdns_plus_default = False

        return self

class Config(ConfigIref, ConfigTags):
    """bdns+ configuration model. levels, volumes and tag definintions. pre-configured with sensible defaults."""


