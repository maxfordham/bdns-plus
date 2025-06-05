"""
Code to document how the tags have been configured.

Used to generate documentation and custom project spec documents.
"""

import json

import yaml

from bdns_plus.models import INSTANCE_REFERENCE_FSTRING, ConfigIref, TagDef


# ------------------------------
def str_presenter(dumper: yaml.Dumper, data: str) -> yaml.representer.Representer.represent_scalar:
    """
    Configure yaml for dumping multiline strings.

    Ref: https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data.
    """
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(
    str,
    str_presenter,
)  # to use with safe_dum
# ------------------------------
# ^ configures yaml for pretty dumping of multiline strings


def data_as_yaml_markdown(data: dict) -> str:
    return f"""
```yaml
{yaml.dump(data, sort_keys=False, indent=2)}
```
"""


def data_as_json_markdown(data: dict) -> str:
    return f"""
```json
{json.dumps(data, sort_keys=False, indent=4)}
```
"""


def summarise_tag_config(tag: TagDef) -> str:
    header = f"**{tag.name}**" + "\n\n" + tag.description
    req = "**Required**: " + "".join(
        [f"{x.prefix}[{x.field_name}]{x.suffix}" for x in tag.fields if not x.allow_none],
    ).strip("/")
    allow = "**Allowed**: " + "".join([f"{x.prefix}[{x.field_name}]{x.suffix}" for x in tag.fields]).strip("/")
    return f"{header}\n\n{req}\n\n{allow}"


def summarise_instance_reference_construction(config_iref: ConfigIref) -> str:
    volume_no_digits, level_no_digits = config_iref.volume_no_digits, config_iref.level_no_digits
    return f"""The instance reference for the BDNS tag is constructed from volume and level data as follows:

- Volumes are represented by {volume_no_digits}no integer digits (volume_id).
- Levels are represented by {level_no_digits}no integer digits (level_id).
- An enumerating integer value is added to ensure uniqueness for a given floor / level (level_instance_id).
- These numbers are joined without delimiter to create a unique number for a given abbreviation:
  - {INSTANCE_REFERENCE_FSTRING.replace("{", "[").replace("}", "]")}"""


def markdown_callout(string: str, callout_type: str = "note", title: str = "", collapse: str = "true") -> str:
    header = "::: {.callout-" + callout_type + " " + f"collapse={collapse}" + "}"
    return f"""{header}
## {title}

{string}
:::"""
