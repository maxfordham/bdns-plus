from .models import Tag, BdnsTag, BdnsTagWithType, Iref, Config
from pydantic import model_validator
import typing as ty
from .iref import serialize_iref

# class IrefBuilder(Iref):
#     @model_validator(mode="after")
#     def build_iref(self) -> ty.Self:
#         data = self.model_dump()
#         iref = serialize_iref(**data)
#         pass

def _gen_iref(data: dict, config: Config | None=None):

    try:
        iref_data= Iref(**data)
    except Exception as e:
        raise ValueError(f"failed to build Iref from data={data} with error={e}")
    
    if config is None:
        config = Config()

    iref = serialize_iref(**iref_data.model_dump(), config=config)
    return iref





# TODO: this feels a bit like repetition of pydantic... could probs use datamodel-code-gen instead...
def validate_tag_data(data: dict, tag: Tag):
    for field in tag.fields:
        value = data.get(field.field_name)
        if value is None:
            for alias in field.field_aliases:
                value = data.get(alias)
                if value is not None:
                    data[field.field_name] = value
                    break
        if field.allow_none is False and data.get(field.field_name) is None:
            e = f"field_name={field.field_name} is required and cannot be None"
            raise ValueError(e)
        if field.validate is not None and value is not None:
            assert field.validate(value)
    return data

def get_tag_data(data: dict, tag: Tag, gen_iref: bool=True, config: Config|None=None):
    if gen_iref:
        iref = _gen_iref(data, config=config)
        data["instance_reference"] = iref

    data = validate_tag_data(data, tag)

    result = {}
    for field in tag.fields:
        value = data.get(field.field_name)
        result[field.field_name] = value
    return result

def build_tag(data: dict, tag: Tag, gen_iref: bool=True, config: Config|None=None):
    tag_data = get_tag_data(data, tag, gen_iref=gen_iref, config=config)
    s = ""
    for field in tag.fields:
        value = tag_data.get(field.field_name)
        if value is None:
            continue # go to next field
        if field.zfill is not None:
            value = str(value).zfill(field.zfill)
        if value is not None:
            s += f"{field.prefix}{value}{field.suffix}"
    return s

def bdns_tag(data: dict, include_type=False, gen_iref: bool=True, config: Config|None=None):
    if include_type:
        tag = BdnsTagWithType()
    else:
        tag = BdnsTag()
    return build_tag(data, tag=tag, gen_iref=gen_iref, config=config)

def instance_tag(data: dict, include_type=False, gen_iref: bool=True, config: Config|None=None):
    return bdns_tag(data, include_type=False)

def type_tag(data: dict):
    return bdns_tag(data, include_type=True)

