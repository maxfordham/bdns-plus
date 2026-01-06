import json

from bdns_plus.models import BdnsTag, BdnsTagWithType, Config, TagDef, TagField
from bdns_plus.tag import Tag, build_tag

f = TagField(
    field_name="instance_reference",
    allow_none=False,
    prefix="-",
    suffix="",
    zfill=1,
)

tag = TagDef(
    name="test",
    description="test tag",
    fields=[
        TagField(field_name="field1"),
        TagField(field_name="field2"),
        TagField(field_name="field3"),
    ],
)


def test_build_tag():
    tag_def = BdnsTag()
    data = {
        "abbreviation": "ABBR",
        "instance_reference": "1",
        "instance_extra": "example",
    }
    tag = build_tag(data, tag=tag_def, gen_iref=False)
    assert isinstance(tag, str)
    assert tag == "ABBR-1_example"

    data = {
        "Abbreviation": "ABBR",
        "TypeReference": 1,
        "InstanceReference": 1,
        "InstanceExtra": "example",
    }
    tag = build_tag(data, tag=tag_def, gen_iref=False)
    assert tag == "ABBR-1_example"
    tag = build_tag(data, tag=BdnsTagWithType(), gen_iref=False)
    assert tag == "ABBR1-1_example"


def test_tag():
    data = {
        "Abbreviation": "ABBR",
        "TypeReference": 1,
        "Level": 1,
        "level_instance": 1,
        "InstanceExtra": "example",
    }
    tag = Tag(data)
    assert tag.bdns == "ABBR-1011_example"
    assert tag.instance == "ABBR/1/1/1/example"
    assert tag.type == "ABBR1"


def test_tag_digital_schedules_data():
    data = {
        "abbreviation": "ASHP",
        "type_reference": 1,
        "function_reference": None,
        "instance_reference": 2,
        "volume_reference": "3",
        "level_reference": "3",
        "volume_level_instance": 5,
    }
    tag = Tag(data)
    assert tag.bdns == "ASHP-3035"
    assert tag.instance == "ASHP/3/3/5"
    assert tag.type == "ASHP1"


def test_custom_tag():
    from pyrulefilter import Rule, RuleSet

    from bdns_plus.models import Config, CustomTagDef

    r = Rule(
        parameter="abbreviation",
        operator="equals",
        value="AHU",
    )
    rule_set = RuleSet(rule=[r], set_type="OR")
    data = {
        "abbreviation": "AHU",
        "type_reference": 1,
        "level": 1,
        "level_instance": 1,
        "instance_extra": "example",
    }
    custom_tag = CustomTagDef(
        description="Custom AHU Tag",
        i_tag=TagDef(
            name="Custom AHU Instance Tag",
            fields=[
                TagField(field_name="abbreviation", suffix="/"),
                TagField(field_name="instance_extra"),
            ],
        ),
        scope=rule_set,
    )
    config = Config(custom_tags=[custom_tag])
    tag = Tag(data, config=config)
    assert tag.type == "AHU1"
    assert tag.instance == "AHU/example"


def test_tag_basement():
    equipment_data = {
        "abbreviation": "AHU",
        "type": 2,
        "level": -1,
        "volume": 1,
        "level_instance": 1,
    }
    tag = Tag(equipment_data)
    bdns = tag.bdns
    assert bdns == "AHU-1991"


def test_type_only_Tag():  # noqa: N802
    data = {
        "Abbreviation": "ABBR",
        "TypeReference": 1,
    }
    tag = Tag(data)
    assert tag.bdns is None
    assert tag.instance is None
    assert tag.type == "ABBR1"


def test_custom_config():
    config = {
        "levels": [
            {"id": 90, "code": "XX", "name": "Not Applicable"},
            {"id": 80, "code": "ZZ", "name": "Multiple Levels"},
            {"id": 91, "code": "B1", "name": "First Level of Basement"},
            {"id": 92, "code": "B2", "name": "Second Level of Basement"},
            {"id": 0, "code": "00", "name": "Level 00"},
            {"id": 1, "code": "01", "name": "Level 01"},
            {"id": 2, "code": "02", "name": "Level 02"},
            {"id": 3, "code": "03", "name": "Level 03"},
            {"id": 4, "code": "04", "name": "Level 04"},
            {"id": 5, "code": "05", "name": "Level 05"},
            {"id": 6, "code": "06", "name": "Level 06"},
            {"id": 7, "code": "07", "name": "Level 07"},
            {"id": 8, "code": "08", "name": "Level 08"},
            {"id": 9, "code": "09", "name": "Level 09"},
            {"id": 10, "code": "10", "name": "Level 10"},
            {"id": 11, "code": "11", "name": "Level 11"},
            {"id": 12, "code": "12", "name": "Level 12"},
            {"id": 81, "code": "M1", "name": "Mezzanine Above Level 01"},
            {"id": 82, "code": "M2", "name": "Mezzanine Above Level 02"},
            {"id": 71, "code": "R1", "name": "Roof Level (R1)"},
            {"id": 72, "code": "R2", "name": "Roof Level (R2)"},
            {"id": 73, "code": "R3", "name": "Roof Level (R3)"},
        ],
        "volumes": [
            {"id": 90, "code": "XX", "name": "Volume Not Applicable"},
            {"id": 80, "code": "ZZ", "name": "Multiple Zones/Sitewide"},
            {"id": 91, "code": "B1", "name": "Main Building (B1)"},
            {"id": 92, "code": "B2", "name": "25m Pool Building (B2)"},
            {"id": 93, "code": "B3", "name": "Indoor Athletics & Walkway (B3)"},
            {"id": 94, "code": "B4", "name": "Former 5-a-side & Bar (B4)"},
            {"id": 95, "code": "B5", "name": "West Stand (B5)"},
            {"id": 96, "code": "B6", "name": "Jubilee Stand (B6)"},
            {"id": 97, "code": "B7", "name": "The Lodge & Attached Ancillary Buildings (B7)"},
            {"id": 98, "code": "B8", "name": "The Houses (B8)"},
            {"id": 1, "code": "L1", "name": "Landscape Zone 1"},
            {"id": 2, "code": "L2", "name": "Landscape Zone 2"},
            {"id": 3, "code": "L3", "name": "Landscape Zone 3"},
            {"id": 4, "code": "L4", "name": "Landscape Zone 4"},
        ],
        "i_tag": {
            "name": "Instance Tag (custom)",
            "description": "Instance tag with custom fields and prefixes",
            "fields": [
                {"field_name": "abbreviation", "suffix": "-"},
                {"field_name": "volume", "suffix": "-"},
                {"field_name": "level", "suffix": "-"},
                {"field_name": "volume_level_instance", "suffix": "/", "zfill": 3},
                {"field_name": "instance_extra", "allow_none": True},
            ],
        },
        "t_tag": {
            "name": "Type Tag (dash)",
            "description": "Type tag with dash between abbreviation and type reference",
            "fields": [
                {"field_name": "abbreviation"},
                {"field_name": "type_reference", "prefix": "/"},
                {"field_name": "type_extra", "prefix": "/", "allow_none": True},
            ],
        },
    }
    data = {
        "abbreviation": "AHU",
        "type_reference": 1,
        "function_reference": None,
        "instance_reference": 1,
        "volume_reference": "B1",
        "level_reference": "B1",
        "volume_level_instance": 1,
    }
    config = json.dumps(config)
    config = Config.model_validate_json(config)
    tag = Tag(data, config=config)

    assert tag.bdns == "AHU-91911"
    assert tag.instance == "AHU-B1-B1-001"
    assert tag.type == "AHU/1"
