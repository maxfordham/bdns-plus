from bdns_plus.tag import build_tag, bdns_tag
from bdns_plus.models import TagField, Tag, BdnsTag

f = TagField(
    field_name="instance_reference",
    allow_none=False,
    prefix="-",
    suffix="",
    zfill=1,
)

tag = Tag(
    name="test",
    description="test tag",
    fields=[
        TagField(field_name="field1"),
        TagField(field_name="field2"),
        TagField(field_name="field3"),
    ]
)

def test_bdns_tag():
    data = {
        "abbreviation": "ABBR",
        "instance_reference": "1",
        "instance_extra": "example",
    }
    tag = bdns_tag(data, gen_iref=False)
    assert isinstance(tag, str)
    assert tag == "ABBR-1_example"

    data = {
        "Abbreviation": "ABBR",
        "TypeReference": 1,
        "InstanceReference": 1,
        "InstanceExtra": "example",
    }
    tag = bdns_tag(data, gen_iref=False)
    assert tag == "ABBR-1_example"
    tag = bdns_tag(data, include_type=True, gen_iref=False)
    assert tag == "ABBR1-1_example"

def test_bdns_tag_gen_iref():

    data = {
        "Abbreviation": "ABBR",
        "TypeReference": 1,
        "Level": 1,
        "level_instance": 1,
        "InstanceExtra": "example",
    }
    tag = bdns_tag(data)
    assert tag == "ABBR-1011_example"
    tag = bdns_tag(data, include_type=True, gen_iref=True)
    assert tag == "ABBR1-1011_example"

