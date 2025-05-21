"""register of default fields for bdns_plus."""
# TODO: maybe load this from json...


def validate_alpha2_country(code: str) -> bool:
    import pycountry

    c = pycountry.countries.get(alpha_2=code)
    if c is None:
        e = f"country code={code} is not valid alpha2"
        raise ValueError(e)
    return True


def country_field(prefix: str = "", suffix: str = "") -> dict:
    return {
        "field_name": "country",
        "field_aliases": ["Country"],
        "allow_none": True,
        "prefix": prefix,
        "suffix": suffix,
        "validator": validate_alpha2_country,
    }


def city_field(prefix: str = "", suffix: str = "") -> dict:
    return {
        "field_name": "city",
        "field_aliases": ["City"],
        "allow_none": True,
        "prefix": prefix,
        "suffix": suffix,
    }


def project_field(prefix: str = "", suffix: str = "") -> dict:
    return {
        "field_name": "project",
        "field_aliases": ["Project"],
        "allow_none": True,
        "prefix": prefix,
        "suffix": suffix,
    }


def abbreviation_field(prefix: str = "", suffix: str = "") -> dict:
    return {
        "field_name": "abbreviation",
        "field_aliases": ["Abbreviation"],
        "allow_none": False,
        "prefix": prefix,
        "suffix": suffix,
    }


def volume_field(prefix: str = "", suffix: str = "") -> dict:
    return {
        "field_name": "volume",
        "field_aliases": ["Volume"],
        "allow_none": False,
        "prefix": prefix,
        "suffix": suffix,
    }


def level_field(prefix: str = "", suffix: str = "") -> dict:
    return {
        "field_name": "level",
        "field_aliases": ["Level"],
        "allow_none": False,
        "prefix": prefix,
        "suffix": suffix,
    }


def level_instance_field(prefix: str = "", suffix: str = "") -> dict:
    return {
        "field_name": "level_iref",
        "field_aliases": ["LevelInstance", "level_instance"],
        "allow_none": False,
        "prefix": prefix,
        "suffix": suffix,
    }


def instance_reference_field(prefix: str = "-", suffix: str = "") -> dict:
    return {
        "field_name": "instance_reference",
        "field_aliases": ["InstanceReference"],
        "allow_none": False,
        "prefix": prefix,
        "suffix": suffix,
    }


def instance_extra_field(prefix: str = "", suffix: str = "") -> dict:
    return {
        "field_name": "instance_extra",
        "field_aliases": ["InstanceExtra"],
        "allow_none": True,
        "prefix": prefix,
        "suffix": suffix,
    }


def type_reference_field(prefix: str = "", suffix: str = "") -> dict:
    return {
        "field_name": "type_reference",
        "field_aliases": ["TypeReference"],
        "allow_none": True,
        "prefix": prefix,
        "suffix": suffix,
    }


def type_extra_field(prefix: str = "", suffix: str = "") -> dict:
    return {
        "field_name": "type_extra",
        "field_aliases": ["TypeExtra"],
        "allow_none": True,
        "prefix": prefix,
        "suffix": suffix,
    }


def bdns_fields(*, include_type: bool = False) -> list[dict]:
    fields = [
        country_field(suffix="-"),
        city_field(suffix="-"),
        project_field(suffix="-"),
        abbreviation_field(),
        instance_reference_field(prefix="-"),
        instance_extra_field(prefix="_"),
    ]
    if include_type:
        fields.insert(4, type_reference_field())
    return fields


def type_fields() -> list[dict]:
    return [
        abbreviation_field(),
        type_reference_field(),
        type_extra_field(prefix="/"),
    ]


def instance_fields(*, include_type: bool = False) -> list[dict]:
    fields = [
        abbreviation_field(suffix="/"),
        volume_field(suffix="/"),
        level_field(suffix="/"),
        level_instance_field(suffix="/"),
        instance_extra_field(),
    ]
    if include_type:
        fields.insert(1, type_reference_field())
    return fields
