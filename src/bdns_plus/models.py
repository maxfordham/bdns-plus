"""data models for bdns_plus."""

from __future__ import annotations

import typing as ty
from enum import Enum

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    ImportString,
    RootModel,
    computed_field,
    model_validator,
)

# if ty.TYPE_CHECKING:
from pyrulefilter import RuleSet

from .abbreviations import get_asset_abbreviations_enum
from .default_fields import (
    bdns_fields,
    instance_fields,
    instance_fields_without_extra,
    type_fields,
    type_fields_without_extra,
)
from .gen_levels_volumes import gen_levels_config, gen_volumes_config

INSTANCE_REFERENCE_FSTRING = "{volume_id}{level_id}{volume_level_instance}"


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
    zfill: int | None = Field(
        None,
        name="Number of digits (zero-padded)",
        title="Number of digits (zero-padded)",
    )
    regex: str | None = None
    validator: ImportString | None = None


class TagDef(BaseModel):  # RootModel
    name: str
    description: str | None = None
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
    id: int = Field(
        ...,
        description="Unique integer ID for the tag. Likely used by the database.",
        name="id",
    )
    code: str | int = Field(
        ...,
        description="Unique Code for the tag. Likely used in drawing references and when modelling.",
        name="code",
    )
    name: str = Field(  # name, title ?
        ...,
        description="Unique Description for the tag. Used in reports / legends.",
        name="name",
    )


class Level(_Base): ...


class Volume(_Base): ...


class Levels(RootModel):
    root: list[Level] = Field(
        ...,
        json_schema_extra={
            "datagrid_index_name": ["name"],
        },
    )


class Volumes(RootModel):
    root: list[Volume] = Field(
        ...,
        json_schema_extra={
            "datagrid_index_name": ["name"],
        },
    )


def default_levels() -> list[Level]:
    return [Level(**x) for x in to_records(gen_levels_config())]


def default_volumes() -> list[Volume]:
    return [Volume(**x) for x in to_records(gen_volumes_config())]


class Iref(BaseModel):
    level: int | str = Field(
        ...,
        validation_alias=AliasChoices(
            "level",
            "level_id",
            "level_number",
            "Level",
            "LevelId",
            "LevelNumber",
            "level_reference",
            "LevelReference",
        ),
    )
    volume_level_instance: int = Field(  # TODO: volume_level_instance
        ...,
        validation_alias=AliasChoices(
            "level_instance",
            "LevelInstance",
            "VolumeLevelInstance",
            "volume_level_instance",
        ),
    )
    volume: int | str = Field(
        1,
        validation_alias=AliasChoices(
            "volume",
            "volume_id",
            "volume_number",
            "Volume",
            "VolumeId",
            "VolumeNumber",
            "volume_reference",
            "VolumeReference",
        ),
    )
    # TODO: allow volume is None and ignore in tag when none.
    #       if zero set to None (e.g. for single volume projects)
    #       this gets around Revits issue about not allowing None.


class TTagData(BaseModel):
    abbreviation: AbbreviationsEnum
    type_reference: int | None = None
    type_extra: str | None = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class ITagData(Iref, TTagData):
    # allow extra to support unknown / custom tag data
    instance_extra: str | None = None


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


class TypeTag(TagDef):  # Default Type Tag
    @model_validator(mode="before")
    @classmethod
    def _set_fields(cls, data: ty.Any) -> dict:  # noqa: ANN401
        di = {}
        di["name"] = "Type Tag"
        di["description"] = tref_tag_def_description
        di["fields"] = type_fields()
        return di


class TypeTagWithoutExtra(TagDef):  # Default Type Tag
    @model_validator(mode="before")
    @classmethod
    def _set_fields(cls, data: ty.Any) -> dict:  # noqa: ANN401
        di = {}
        di["name"] = "Type Tag"
        di["description"] = tref_tag_def_description
        di["fields"] = type_fields_without_extra()
        return di


iref_tag_def_description = (
    "Default Tag Definition for indentifying a unique instance of equipment within a building. "
    "Expected to be used for adding equipment references to drawings, reports and legends. "
)


class InstanceTag(TagDef):  # Default Instance Tag
    @model_validator(mode="before")
    @classmethod
    def _set_fields(cls, data: ty.Any) -> dict:  # noqa: ANN401
        di = {}
        di["name"] = "Instance Tag"
        di["description"] = iref_tag_def_description
        di["fields"] = instance_fields(include_type=False)
        return di


class InstanceTagWithoutExtra(TagDef):
    @model_validator(mode="before")
    @classmethod
    def _set_fields(cls, data: ty.Any) -> dict:  # noqa: ANN401
        di = {}
        di["name"] = "Instance Tag"
        di["description"] = iref_tag_def_description
        di["fields"] = instance_fields_without_extra(include_type=False)
        return di


class ConfigIref(BaseModel):
    """defines params required to generate an instance ref. levels and volumes."""

    levels: list[Level] = Field([])
    volumes: list[Volume] = Field([])
    level_identifier_type: IdentifierType = IdentifierType.code
    volume_identifier_type: IdentifierType = IdentifierType.code
    map_volume_level: dict[int, int] | None = None  # allows for restricting volumes to known levels
    iref_fstring: ty.Literal["{volume_id}{level_id}{volume_level_instance}"] = (
        INSTANCE_REFERENCE_FSTRING  # TODO: delete
    )
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

    @computed_field
    @property
    def level_ids(self) -> list[int]:
        return [x.id for x in self.levels]

    @computed_field
    @property
    def volume_ids(self) -> list[int]:
        return [x.id for x in self.volumes]

    @computed_field
    @property
    def level_no_digits(self) -> int | None:
        if not self.levels:
            return None
        return max([len(str(x)) for x in self.level_ids])

    @computed_field
    @property
    def volume_no_digits(self) -> int | None:
        if not self.levels:
            return None
        return max([len(str(x)) for x in self.volume_ids])

    @computed_field
    @property
    def no_levels(self) -> int:
        return len(self.levels)

    @computed_field
    @property
    def no_volumes(self) -> int:
        return len(self.volumes)


class CustomTagDef(BaseModel):
    """Custom Tag Definition for user-defined tags that are do be applied to filtered set of items."""

    description: str | None = None
    scope: RuleSet | None = None
    i_tag: TagDef | type[TagDef] | None = None
    t_tag: TagDef | type[TagDef] | None = None


class CustomTagDefList(RootModel):
    root: list[CustomTagDef]


class ConfigTags(BaseModel):
    """defines tag definitions. bdns, instance and type tags. pre-configured with sensible defaults."""

    bdns_tag: type[BdnsTag | BdnsTagWithType] = BdnsTag()  # FIXED
    i_tag: TagDef | type[TagDef] = InstanceTag()
    t_tag: TagDef | type[TagDef] = TypeTag()
    custom_tags: list[CustomTagDef] = Field(
        None,
        description="Custom Tag Definitions for user-defined tags that are do be applied to filtered set of items.",
    )
    is_bdns_plus_default: bool = True
    drop_if_single_volume: bool = True

    @model_validator(mode="after")
    def _check_is_bdns_plus_default(self) -> ty.Self:
        check_default = [
            bool(isinstance(i, c))
            for i, c in zip([self.bdns_tag, self.i_tag, self.t_tag], [BdnsTag, InstanceTag, TypeTag], strict=True)
        ]
        if False in check_default:
            self.is_bdns_plus_default = False

        return self

    @model_validator(mode="after")
    def _drop_if_single_volume(self) -> ty.Self:
        if self.no_volumes == 1 and self.drop_if_single_volume:
            data = self.i_tag.model_dump(mode="json")
            data["fields"] = [f for f in data["fields"] if f["field_name"] != "volume"]
            self.i_tag = TagDef(**data)
        return self


class BaseConfig(ConfigTags, ConfigIref):
    """Base Config is an identical model to Config Tags, except without default values for i_tag and t_tag."""

    i_tag: TagDef | type[TagDef] | None = None
    t_tag: TagDef | type[TagDef] | None = None


class Config(ConfigTags, ConfigIref):
    """bdns+ configuration model. levels, volumes and tag definitions. pre-configured with sensible defaults."""


class GenDefinition(BaseModel):
    abbreviation: AbbreviationsEnum | list[AbbreviationsEnum]
    types: list[int | None] | None = None
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
