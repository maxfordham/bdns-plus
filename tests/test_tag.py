from bdns_plus.models import BdnsTag, BdnsTagWithType, TagDef, TagField
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


def test_Tag():  # noqa: N802
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


def test_type_only_Tag():  # noqa: N802
    data = {
        "Abbreviation": "ABBR",
        "TypeReference": 1,
    }
    tag = Tag(data)
    assert tag.bdns is None
    assert tag.instance is None
    assert tag.type == "ABBR1"
