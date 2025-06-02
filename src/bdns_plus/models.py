"""data models for bdns_plus."""

from __future__ import annotations

import typing as ty
from enum import Enum

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, ImportString, model_validator

from .abbreviations import get_asset_abbreviations_enum
from .default_fields import bdns_fields, instance_fields, type_fields
from .gen_levels_volumes import gen_levels_config, gen_volumes_config

INSTANCE_REFERENCE_FSTRING = "{volume_id}{level_id}{level_instance_id}"


class StrEnum(str, Enum):
    pass


def to_records(data: list[list]) -> list[dict]:
    return [dict(zip(data[0], x, strict=False)) for x in data[1:]]


AbbreviationsEnum = StrEnum("AbbreviationsEnum", get_asset_abbreviations_enum())


# TODO: this feels a bit like repetition of pydantic... could probs use datamodel-code-gen instead...
class TagField(BaseModel):
    field_name: str
    field_aliases: list[str] = []
    allow_none: bool = False
    prefix: str = ""
    suffix: str = ""
    zfill: int | None = None
    regex: str | None = None
    validator: ImportString | None = None  # ty.Callable[[ty.Any], bool] | None = None


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
    code = "code"
    name = "name"


class TagType(str, Enum):
    bdns = "bdns"
    instance = "instance"
    type = "type"


class _Base(BaseModel):
    id: int = Field(..., description="Unique integer ID for the tag. Likely used by the database.")
    code: str | int = Field(
        ...,
        description="Unique Code for the tag. Likely used in drawing references and when modelling.",
    )
    name: str = Field(  # name, title ?
        ...,
        description="Unique Description for the tag. Used in reports / legends.",
    )


class Level(_Base): ...


class Volume(_Base): ...


def default_levels() -> list[Level]:
    return [Level(**x) for x in to_records(gen_levels_config())]


def default_volumes() -> list[Volume]:
    return [Volume(**x) for x in to_records(gen_volumes_config())]


class Iref(BaseModel):
    level: int | str = Field(
        ...,
        validation_alias=AliasChoices("level", "level_id", "level_number", "Level", "LevelId", "LevelNumber"),
    )
    level_iref: int = Field(  # TODO: volume_level_instance
        ...,
        validation_alias=AliasChoices("level_instance", "LevelInstance", "VolumeLevelInstance", "level_iref"),
    )
    volume: int | str = Field(
        1,
        validation_alias=AliasChoices("volume", "volume_id", "volume_number", "Volume", "VolumeId", "VolumeNumber"),
    )


class TTagData(BaseModel):
    abbreviation: AbbreviationsEnum
    type_reference: int | None = None
    type_extra: str | None = None

    model_config = ConfigDict(allow_extra=True, populate_by_name=True)


class ITagData(Iref, TTagData):
    # allow extra to support unknown / custom tag data
    pass


class BdnsTag(TagDef):
    @model_validator(mode="before")
    @classmethod
    def _set_fields(cls, data: ty.Any) -> dict:  # noqa: ANN401
        di = {}
        di["name"] = "BDNS Tag"
        di["description"] = "TagDef Definition in accordance with Building Data Naming System"
        di["fields"] = bdns_fields(include_type=False)
        return di


class BdnsTagWithType(TagDef):
    @model_validator(mode="before")
    @classmethod
    def _set_fields(cls, data: ty.Any) -> dict:  # noqa: ANN401
        di = {}
        di["name"] = "BDNS Tag (inc. Type)"
        di["description"] = "TagDef Definition in accordance with Building Data Naming System. Type included."
        di["fields"] = bdns_fields(include_type=True)
        return di


tref_tag_def_description = (
    "Default Tag Definition for indentifying a unique type of equipment, "
    "there is likely to be many instances of a type in the building. "
    "Expected to be used when a unique reference to every item is not required. "
    "For example, a light fitting type that may be used in many locations."
)


class TypeTag(TagDef):
    @model_validator(mode="before")
    @classmethod
    def _set_fields(cls, data: ty.Any) -> dict:  # noqa: ANN401
        di = {}
        di["name"] = "Type Tag"
        di["description"] = tref_tag_def_description
        di["fields"] = type_fields()
        return di


iref_tag_def_description = (
    "Default Tag Definition for indentifying a unique instance of equipment within a building. "
    "Expected to be used for adding equipment references to drawings, reports and legends. "
)


class InstanceTag(TagDef):
    @model_validator(mode="before")
    @classmethod
    def _set_fields(cls, data: ty.Any) -> dict:  # noqa: ANN401
        di = {}
        di["name"] = "Instance Tag"
        di["description"] = iref_tag_def_description
        di["fields"] = instance_fields(include_type=False)
        return di


class ConfigIref(BaseModel):
    """defines params required to generate an instance ref. levels and volumes."""

    levels: list[Level] = Field([])
    volumes: list[Volume] = Field([])
    level_identifier_type: IdentifierType = IdentifierType.code
    volume_identifier_type: IdentifierType = IdentifierType.code
    map_volume_level: dict[int, int] | None = None  # allows for restricting volumes to known levels
    level_no_digits: int | None = None  # TODO: computed field
    no_levels: int | None = None  # TODO: computed field
    no_volumes: int | None = None  # TODO: computed field
    volume_no_digits: int | None = None  # TODO: computed field
    iref_fstring: ty.Literal["{volume_id}{level_id}{level_instance_id}"] = INSTANCE_REFERENCE_FSTRING
    is_default_levels: bool = False  # TODO: required?
    is_default_volumes: bool = False  # TODO: required?

    @model_validator(mode="after")
    def _check_volumes_and_levels(self) -> ty.Self:
        if len(self.levels) == 0:
            self.is_default_levels = True
            self.levels = default_levels()
        if len(self.volumes) == 0:
            self.is_default_volumes = True
            self.volumes = default_volumes()
        return self

    @model_validator(mode="after")
    def _get_no_digits(self) -> ty.Self:
        level_ids = [len(str(x.id)) for x in self.levels]
        self.level_no_digits = max(level_ids)
        volume_ids = [len(str(x.id)) for x in self.volumes]
        self.volume_no_digits = max(volume_ids)
        return self

    @model_validator(mode="after")
    def _get_nos(self) -> ty.Self:
        self.no_levels = len(self.levels)
        self.no_volumes = len(self.volumes)
        return self


class ConfigTags(BaseModel):
    """defines tag definitions. bdns, instance and type tags. pre-configured with sensible defaults."""

    bdns_tag: type[BdnsTag | BdnsTagWithType] = BdnsTag()  # FIXED
    i_tag: type[TagDef] = InstanceTag()
    t_tag: type[TagDef] = TypeTag()
    custom_i_tags: dict[str, type[TagDef]] = {}  # AbbreviationsEnum
    custom_t_tags: dict[str, type[TagDef]] = {}  # AbbreviationsEnum
    map_custom_i_tags: dict[str, str] = {}
    map_custom_t_tags: dict[str, str] = {}
    is_bdns_plus_default: bool = True

    @model_validator(mode="after")
    def _check_is_bdns_plus_default(self) -> ty.Self:
        check_default = [
            bool(isinstance(i, c))
            for i, c in zip([self.bdns_tag, self.i_tag, self.t_tag], [BdnsTag, InstanceTag, TypeTag], strict=True)
        ]
        if False in check_default:
            self.is_bdns_plus_default = False

        return self


class Config(ConfigIref, ConfigTags):
    """bdns+ configuration model. levels, volumes and tag definitions. pre-configured with sensible defaults."""


class GenDefinition(BaseModel):
    abbreviation: AbbreviationsEnum | list[AbbreviationsEnum]
    no_items: int = 1
    on_levels: list | None = None
    on_volumes: list | None = None


class GenLevelsVolumes(BaseModel):
    level_min: int = -1
    level_max: int = 3
    no_volumes: int = 1


class GenExampleProject(GenLevelsVolumes):
    """Example project for bdns_plus."""

    name: str = "Example Project"
    description: str | None = None
