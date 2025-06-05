# %% [markdown]
# ---
# title: Tag Builder
# format:
#   html:
#     code-fold: true
# ---

# %% [markdown]
"""
At its simplest, bdns-plus can be used to build tags from data.
The `simple_tag` function takes a dictionary of data and a `TagDef` object, and returns a tag string.
It is directly analogous to the way that tags work in Revit, and the `TagDef` class is a direct port of the Revit tag definition.

The example below shows how an instance tag can be built from a dictionary of data.
"""

# %%
from IPython.display import Markdown, display

from bdns_plus.docs import data_as_json_markdown, data_as_yaml_markdown, markdown_callout, summarise_tag_config
from bdns_plus.models import TagDef, TagField
from bdns_plus.tag import simple_tag

tag_def = {
    "name": "Tag Definition for Ventilation Instances",
    "description": "a example tag definition for ventilation instances",
    "fields": [
        {
            "field_name": "abbreviation",
            "field_aliases": [
                "Abbreviation",
            ],
            "allow_none": False,
            "prefix": "",
            "suffix": "",
            "zfill": None,
            "regex": None,
            "validator": None,
        },
        {
            "field_name": "volume",
            "field_aliases": [
                "Volume",
            ],
            "allow_none": False,
            "prefix": ".",
            "suffix": "",
            "zfill": None,
            "regex": None,
            "validator": None,
        },
        {
            "field_name": "level",
            "field_aliases": [
                "Level",
            ],
            "allow_none": False,
            "prefix": ".",
            "suffix": "",
            "zfill": 2,
            "regex": None,
            "validator": None,
        },
        {
            "field_name": "level_iref",
            "field_aliases": [
                "VolumeLevelInstance",
            ],
            "allow_none": False,
            "prefix": ".",
            "suffix": "",
            "zfill": 2,
            "regex": None,
            "validator": None,
        },
    ],
}

itag_def = TagDef(**tag_def)  # or use TagDef.from_dict(tag_def)

data = {"abbreviation": "AHU", "level": "GF", "level_iref": 1, "volume": "N"}
tag_string = simple_tag(data, tag=itag_def)

yaml_str = data_as_json_markdown(itag_def.model_dump(mode="json"))
import pathlib

pathlib.Path("example")

title = "Tag Definition as json data. Can be loaded dynamically and configured per project."
display(
    Markdown(markdown_callout(yaml_str, title=title)),
)  # This will print the header
display(Markdown(summarise_tag_config(itag_def)))  # This will print the tag configuration summary
display(Markdown("**Example:**"))  # This will print the tag string
display(Markdown(data_as_yaml_markdown(data)))  # This will print the data as YAML markdown
print(tag_string)  # Output: AHU.GF.01.N


# %% [markdown]
"""
## Serializing Unique Numeric Identifiers

In the example above, it is demonstrated how a tag can be built from a dictionary of data.

"""
