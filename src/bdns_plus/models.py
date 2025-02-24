import typing as ty
from enum import Enum
from pydantic import BaseModel, RootModel, Field, model_validator, AliasChoices
from .config import gen_levels_config, gen_volumes_config
from pydantic import BeforeValidator

INSTANCE_REFERENCE_FSTRING = "{volume_id}{level_id}{level_instance_id}"

def to_records(data):
    return [dict(zip(data[0], x)) for x in data[1:]]

class ConfigType(str, Enum):
    level = "level"
    volume = "volume"
    level_instance = "level_instance"

class IdentifierType(str, Enum):
    id = "id"
    number = "number"
    name = "name"

class Level(BaseModel):
    level: int
    level_id: int
    level_name: str

class Volume(BaseModel):
    volume: int
    volume_id: int
    volume_name: str

def default_levels():
    return [Level(**x) for x in to_records(gen_levels_config())]

def default_volumes():
    return [Volume(**x) for x in to_records(gen_volumes_config())]

class Iref(BaseModel):
    level: int = Field(..., validation_alias=AliasChoices('level', 'level_id', "level_number", "Level", "LevelId", "LevelNumber"))  
    level_iref: int = Field(..., validation_alias=AliasChoices('level_instance', 'LevelInstance', "VolumeLevelInstance", "level_iref"))  
    volume: int = Field(1, validation_alias=AliasChoices('volume', 'volume_id', "volume_number", "Volume", "VolumeId", "VolumeNumber")) 
 
class Config(BaseModel):
    levels: list[Level] = Field(default_levels())
    volumes: list[Volume] = Field(default_volumes())
    map_volume_level: ty.Optional[dict[int, int]] = None # allows for restricting volumes to known levels
    level_no_digits: int | None = None
    volume_no_digits: int | None = None
    iref_fstring: ty.Literal["{volume_id}{level_id}{level_instance_id}"] = INSTANCE_REFERENCE_FSTRING

    @model_validator(mode='after')
    def get_no_digits(self) -> ty.Self:
        level_ids = [len(str(x.level_id)) for x in self.levels]
        self.level_no_digits = max(level_ids)
        volume_ids = [len(str(x.volume_id)) for x in self.volumes]
        self.volume_no_digits = max(volume_ids)
        return self


# TODO: this feels a bit like repetition of pydantic... could probs use datamodel-code-gen instead...
class TagField(BaseModel):
    field_name: str
    field_aliases: list[str] = []
    allow_none: bool = False
    prefix: str = ""
    suffix: str = ""
    zfill: int | None = None
    regex: str | None = None
    validate: ty.Callable[[ty.Any], bool] | None = None

class Tag(BaseModel):
    name: str
    description: str
    fields: list[TagField]

def validate_alpha2_country(code:str):
    import pycountry
    c = pycountry.countries.get(alpha_2=code)
    if c is None:
        raise ValueError(f"country code={code} is not valid alpha2")
        # return False
    else:
        return True
    

# TODO: move below to tag.py?

def bdns_fields(include_type=False):
    fields = [
        TagField(field_name="country", field_aliases=["Country"], allow_none=True, prefix="", suffix="-", validate=validate_alpha2_country),
        TagField(field_name="city", field_aliases=["City"], allow_none=True, prefix="", suffix="-"),
        TagField(field_name="project", field_aliases=["Project"], allow_none=True, prefix="", suffix="-"),
        TagField(field_name="abbreviation", field_aliases=["Abbreviation"], allow_none=False, prefix="", suffix=""),
        TagField(field_name="instance_reference", field_aliases=["InstanceReference"], allow_none=False, prefix="-", suffix=""),
        TagField(field_name="instance_extra", field_aliases=["InstanceExtra"], allow_none=True, prefix="_", suffix=""),
    ]
    if include_type:
        fields.insert(4, TagField(field_name="type_reference", field_aliases=["TypeReference"], allow_none=True, prefix="", suffix=""))
    return fields

class BdnsTag(Tag):

    @model_validator(mode='before')
    @classmethod
    def set_fields(cls, data: ty.Any) -> dict: 
        di = {} 
        di["name"]= "bdns"
        di["description"] = "Tag Definition in accordance with Building Data Naming System"
        di["fields"] =  bdns_fields(include_type=False)
        return di

class BdnsTagWithType(BdnsTag):

    @model_validator(mode='before')
    @classmethod
    def set_fields(cls, data: ty.Any) -> dict: 
        di = {} 
        di["name"]= "bdns"
        di["description"] = "Tag Definition in accordance with Building Data Naming System"
        di["fields"] =  bdns_fields(include_type=True)
        return di