# %% [markdown]
# ---
# title: Tags
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
# | echo: false
import pathlib

from IPython.display import Markdown, display

from bdns_plus.docs import data_as_json_markdown, data_as_yaml_markdown, markdown_callout, summarise_tag_config
from bdns_plus.models import (
    INSTANCE_REFERENCE_FSTRING,
    BdnsTag,
    BdnsTagWithType,
    ConfigIref,
    ConfigTags,
    InstanceTag,
    TagDef,
    TagField,
    TypeTag,
)
from bdns_plus.tag import simple_tag


def summarise_instance_reference_construction(config_iref: ConfigIref):
    volume_no_digits, level_no_digits = config_iref.volume_no_digits, config_iref.level_no_digits
    return f"""The instance reference for the BDNS tag is constructed from volume and level data as follows:

- Volumes are represented by {volume_no_digits}no integer digits (volume_id).
- Levels are represented by {level_no_digits}no integer digits (level_id).
- An enumerating integer value is added to ensure uniqueness for a given floor / level (level_instance_id).
- These numbers are joined without delimiter to create a unique number for a given abbreviation:
  - {INSTANCE_REFERENCE_FSTRING.replace("{", "[").replace("}", "]")}"""


# %% [markdown]
"""
## Default Tag Definitions

The default tag definitions are available in the `ConfigTags` class.
"""

# %%
# | echo: false
display(Markdown(summarise_tag_config(TypeTag())))
display(Markdown(summarise_tag_config(InstanceTag())))
display(Markdown(summarise_tag_config(BdnsTag())))

config_iref = ConfigIref()
Markdown(summarise_instance_reference_construction(config_iref))

# %% [markdown]
"""
## Custom Tag Definitions

::: {.callout-tip}
Refer to [reformat-type-and-instance-tags](examples/reformat-type-and-instance-tags) for a more comprehensive example.
:::

"""

# %%
tag_def = {
    "name": "Ventilation Equipment Instances",
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

itag_def = TagDef(**tag_def)

data = {"abbreviation": "AHU", "level": "GF", "level_iref": 1, "volume": "N"}
tag_string = simple_tag(data, tag=itag_def)
json_str = data_as_json_markdown(itag_def.model_dump(mode="json"))


title = "Tag Definition as json data. Can be loaded dynamically and configured per project."
display(
    Markdown(markdown_callout(json_str, title=title)),
)
display(Markdown(summarise_tag_config(itag_def)))  # This will print the tag configuration summary
display(Markdown("**Example:**"))  # This will print the tag string
display(Markdown(data_as_yaml_markdown(data)))  # This will print the data as YAML markdown
display(Markdown(f"**Tag String:** `{tag_string}`"))  # This will print the tag string


# %% [markdown]
"""
## Custom Tags for Specific Equipment Types

::: {.callout-tip}
Refer to [custom-nomenclature-for-vent-equipment](examples/custom-nomenclature-for-vent-equipment)
for a more comprehensive example.
:::

::: {.callout-warning title="not reccommended"}
Ideally tags should be consistent across all equipment types.
:::

The `bdns-tag`, `type-tag` and `instance-tag` and generated for every item of equipment in the project,
and are globally defined and unique for the project.

In an ideal world, the way that tags are constructed is consistent across all equipment types.
However projects are messy, there are cases where specific equipment types require custom tags.
In these cases it is possible to define custom tags with custom scopes.

### How to Define the Scope of a Custom Tag

A RuleSet can be used to define the scope of a custom tag. (For more info refer to [pyrulefilter](https://maxfordham.github.io/pyrulefilter/).
It allows the user to define a set of rules that are used to check the equipment data,
and returns a boolean value indicating if a RuleSet matches the data.
At Max Fordham, RuleSets are also used to define what equipment should be shown in a schedule,
so by extension it is then possible to apply custom tags to every equipment item shown within a schedule.

#### RuleSet Definition
"""

# %%
import jsonschema2md
from IPython.display import Markdown
from pyrulefilter import RuleSet

parser = jsonschema2md.Parser(
    examples_as_yaml=False,
    show_examples="all",
)
md_lines = parser.parse_schema(RuleSet.model_json_schema())
Markdown("".join(md_lines[2:]))


# %% [markdown]
"""
#### Example

In this example, we show how a rule can be defined to give specific equipment
a different tag if the data that defines that equipment matches a rule.

The Exammple below shows ventilation equipment tagged in the normal way,
but we'll assume that AHUs must be named by their volume only (lets pretend that the project is a refurbishment and the AHU names already exist).

In the code below you can see how a ruleset is defined to filter out the equipment requiring a custom tag.
"""

# %%
import pandas as pd
from pyrulefilter import Rule, RuleSet, ruleset_check_dicts

from bdns_plus.docs import get_idata_tag_table
from bdns_plus.gen_idata import batch_gen_idata
from bdns_plus.models import Config, CustomTagDef, GenDefinition, TagDef


def get_idata_tag_df(header: list[tuple], idata: list[dict]) -> pd.DataFrame:
    annotated_cols = pd.MultiIndex.from_tuples(header)
    df_tags = pd.DataFrame(idata).sort_values(by=["level"]).reset_index(drop=True)
    df_tags.columns = annotated_cols
    return df_tags


gen_def1 = GenDefinition(abbreviation=["AHU"], no_items=1, on_levels=[0], on_volumes=[1])
gen_def2 = GenDefinition(abbreviation=["MVHR", "TEF"], no_items=1, on_levels=[1, 2, 3], on_volumes=[1])
gen_def3 = GenDefinition(abbreviation=["KEF", "FAN"], no_items=2, on_levels=[0], on_volumes=[1])
gen_defs = [gen_def1, gen_def2, gen_def3]
idata = batch_gen_idata(gen_defs, config_iref)


r = Rule(
    parameter="abbreviation",
    operator="equals",
    value="AHU",
)
rule_set = RuleSet(rule=[r], set_type="OR")
custom_tag_def = TagDef(
    name="Custom AHU Instance Tag",
    fields=[
        TagField(field_name="abbreviation", suffix="-"),
        TagField(field_name="volume", prefix="Volume"),
    ],
)
custom_tag = CustomTagDef(
    description="Custom AHU Tag",
    i_tag=custom_tag_def,
    t_tag=custom_tag_def,  # just override it to be the same
    scope=rule_set,
)
config = Config(custom_tags=[custom_tag])
display(get_idata_tag_df(*get_idata_tag_table(idata, config=config)))
