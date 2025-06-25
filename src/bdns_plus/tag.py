"""contains functions to build string tags from data."""

from __future__ import annotations

import logging
from enum import Enum

from pydantic import ValidationError
from pyrulefilter import ruleset_check_dict

from .iref import serialize_iref
from .models import Config, ConfigIref, Iref, ITagData, TagDef, TTagData

logger = logging.getLogger(__name__)


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
        if field.validator is not None and value is not None:
            assert field.validator(value)
    return data


def _get_tag_data(  # BUG: this is modifying the data dict in place, which is not ideal
    data: dict | ITagData | TTagData,
    tag: TagDef,
    *,
    gen_iref: bool = True,
    config: ConfigIref | None = None,
) -> dict:
    """Get tag data from data."""
    if isinstance(data, (ITagData, TTagData)):
        data = data.model_dump()
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


def _build_tag(data: dict, tag: TagDef) -> str:
    """Build tag string from data."""
    s = ""
    for field in tag.fields:
        value = data.get(field.field_name)
        if value is None:
            continue  # go to next field
        if isinstance(value, Enum):
            value = value.value
        if field.zfill is not None:
            value = str(value).zfill(field.zfill)
        if value is not None:
            s += f"{field.prefix}{value}{field.suffix}"
    return s.strip("_/-.")


def simple_tag(
    data: dict | ITagData | TTagData,
    tag: TagDef,
) -> str:
    """Build tag string from data. By default, generates an iref on the fly."""
    tag_data = _get_tag_data(data, tag, gen_iref=False, config=None)
    return _build_tag(tag_data, tag)


def build_tag(
    data: dict | ITagData | TTagData,
    tag: TagDef,
    *,
    gen_iref: bool = True,
    config: ConfigIref | None = None,
    is_clean_data: bool = False,
) -> str:
    """Build tag string from data. By default, generates an iref on the fly."""
    tag_data = _get_tag_data(data, tag, gen_iref=gen_iref, config=config) if not is_clean_data else data
    return _build_tag(tag_data, tag)


def bdns_tag(data: dict, *, config: Config | None = None, gen_iref: bool = True, is_clean_data: bool = False) -> str:
    if config is None:
        config = Config()
    return build_tag(data, tag=config.bdns_tag, config=config, gen_iref=gen_iref, is_clean_data=is_clean_data)


def instance_tag(
    data: dict,
    *,
    config: Config | None = None,
    gen_iref: bool = True,
    is_clean_data: bool = False,
) -> str:
    if config is None:
        config = Config()

    return build_tag(data, tag=config.i_tag, config=config, gen_iref=gen_iref, is_clean_data=is_clean_data)


def type_tag(data: dict, *, config: Config | None = None, is_clean_data: bool = False) -> str:
    if config is None:
        config = Config()
    return build_tag(data, tag=config.t_tag, config=config, gen_iref=False, is_clean_data=is_clean_data)


# TODO:
# create another class for batch tagging thousands of items


class Tag:
    """TagDef class with bdns_tag, i_tag, and t_tag properties."""

    def __init__(self, data: dict, *, config: Config | None = None, gen_iref: bool = True) -> None:
        """Init TagDef class."""
        if config is None:
            config = Config()
        if not isinstance(data, dict):
            data = data.model_dump(mode="json")
        self.is_custom = False
        self.config = config
        self.data = data
        self.gen_iref = gen_iref
        self.custom_i_tag, self.custom_t_tag = self._get_custom_tags()

    def _get_custom_tags(self) -> str:
        """Return custom tag string from data."""
        if not self.config.custom_tags:
            return None, None
        logger.info("multiple custom tags found, finding matches")
        matches = [ruleset_check_dict(self.data, r.scope) for r in self.config.custom_tags]
        if not any(matches):
            logger.info("no custom tags matched, returning None")
            return None, None
        if len(matches) > 1:
            logger.error(f"multiple custom tags matched: {matches}, returning first match")

        index = matches.index(True)
        self.is_custom = True
        return self.config.custom_tags[index].i_tag, self.config.custom_tags[index].t_tag

    @property
    def bdns(self) -> str:
        """Return bdns tag string from data."""
        # config.bdns_tag)
        try:
            data = _get_tag_data(self.data, self.config.bdns_tag, gen_iref=self.gen_iref, config=self.config)
            return bdns_tag(data, config=self.config, gen_iref=self.gen_iref, is_clean_data=True)
        except ValidationError as e:
            _e = f"failed to build bdns tag from data={self.data} with error={e}"
            logger.warning(_e)
            return None

    @property
    def instance(self) -> str:
        """Return bdns tag string from data."""
        try:
            if self.custom_i_tag:
                data = _get_tag_data(self.data, self.custom_i_tag, gen_iref=self.gen_iref, config=self.config)
                return build_tag(data, self.custom_i_tag, gen_iref=self.gen_iref, is_clean_data=True)

            data = _get_tag_data(self.data, self.config.i_tag, gen_iref=self.gen_iref, config=self.config)
            return instance_tag(data, config=self.config, gen_iref=self.gen_iref, is_clean_data=True)
        except ValidationError as e:
            _e = f"failed to build bdns tag from data={self.data} with error={e}"
            logger.warning(_e)
            return None

    @property
    def type(self) -> str:
        """Return bdns tag string from data."""
        if self.custom_t_tag:
            data = _get_tag_data(self.data, self.custom_i_tag, gen_iref=False, config=self.config)
            return build_tag(data, self.custom_t_tag, gen_iref=False, is_clean_data=True)
        data = _get_tag_data(self.data, self.config.t_tag, gen_iref=False, config=self.config)
        return type_tag(data, config=self.config, is_clean_data=True)

    @property
    def summary(self) -> str:
        """Return a summary of the tags."""
        bdns = self.bdns
        instance = self.instance
        type_ = self.type
        return (
            f"**BDNS**: {bdns}\n\n**Instance**: {instance}\n\n**Type**: {type_}" if bdns else "No BDNS tag available."
        )
