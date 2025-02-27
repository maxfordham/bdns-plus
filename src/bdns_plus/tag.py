"""contains functions to build string tags from data."""
from __future__ import annotations

from .iref import serialize_iref
from .models import Config, ConfigIref, Iref, TagDef


def _gen_iref(data: dict, config: ConfigIref | None = None) -> Iref:
    try:
        iref_data = Iref(**data)
    except TypeError as e:
        _e = f"failed to build Iref from data={data} with error={e}"
        raise TypeError(_e) from e

    if config is None:
        config = Config()

    return serialize_iref(**iref_data.model_dump(), config=config)


# TODO: this feels a bit like repetition of pydantic... could probs use datamodel-code-gen instead...
def _validate_tag_data(data: dict, tag: TagDef) -> dict:
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


def _get_tag_data(
    data: dict, tag: TagDef, *, gen_iref: bool = True, config: ConfigIref | None = None,
) -> dict:


    if gen_iref:
        try:
            iref_data = Iref(**data)
        except TypeError as e:
            _e = f"failed to build Iref from data={data} with error={e}"
            raise TypeError(_e) from e
        if config is None:
            config = ConfigIref()
        iref = serialize_iref(**iref_data.model_dump(), config=config)
        data["instance_reference"] = iref
        data = data | iref_data.model_dump()

    data = _validate_tag_data(data, tag)

    result = {}
    for field in tag.fields:
        value = data.get(field.field_name)
        result[field.field_name] = value
    return result


def build_tag(
    data: dict, tag: TagDef, *, gen_iref: bool = True, config: ConfigIref | None = None, is_clean_data: bool = False,
) -> str:
    """Build tag string from data."""
    tag_data = _get_tag_data(data, tag, gen_iref=gen_iref, config=config) if not is_clean_data else data
    s = ""
    for field in tag.fields:
        value = tag_data.get(field.field_name)
        if value is None:
            continue  # go to next field
        if field.zfill is not None:
            value = str(value).zfill(field.zfill)
        if value is not None:
            s += f"{field.prefix}{value}{field.suffix}"
    return s

def bdns_tag(data: dict, *, config: Config | None = None, gen_iref: bool = True, is_clean_data: bool = False) -> str:
    if config is None:
        config = Config()
    return build_tag(data, tag=config.bdns_tag, config=config, gen_iref=gen_iref, is_clean_data = is_clean_data)

def instance_tag(data: dict, *, config: Config | None = None, gen_iref: bool = True, is_clean_data: bool = False) -> str:
    if config is None:
        config = Config()
    return build_tag(data, tag=config.i_tag, config=config, gen_iref=gen_iref, is_clean_data = is_clean_data)

def type_tag(data: dict, *, config: Config | None = None, is_clean_data: bool = False) -> str:
    if config is None:
        config = Config()
    return build_tag(data, tag=config.t_tag, config=config, gen_iref=False, is_clean_data = is_clean_data)

class Tag:
    """TagDef class with bdns_tag, i_tag, and t_tag properties."""

    def __init__(self, data: dict, *, config: Config | None = None, gen_iref: bool = True) -> None:
        """Init TagDef class."""
        if config is None:
            config = Config()

        # merge all data required for all tags
        _data = {}
        for tag, _gen_iref in zip([config.bdns_tag, config.i_tag, config.t_tag], [gen_iref, gen_iref, False]):
            _data = _data | _get_tag_data(data, tag, gen_iref=_gen_iref, config=config)
        self.data = _data

        self.config = config
        self.gen_iref = gen_iref

    @property
    def bdns(self) -> str:
        """Return bdns tag string from data."""
        return bdns_tag(self.data, config=self.config, gen_iref=self.gen_iref, is_clean_data=True)

    @property
    def instance(self) -> str:
        """Return bdns tag string from data."""
        return instance_tag(self.data, config=self.config, gen_iref=self.gen_iref, is_clean_data=True)

    @property
    def type(self) -> str:
        """Return bdns tag string from data."""
        return type_tag(self.data, config=self.config, is_clean_data=True)

