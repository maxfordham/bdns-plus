"""
Code to document how the tags have been configured.

Used to generate documentation and custom project spec documents.
"""

import logging

logger = logging.getLogger(__name__)

try:
    import ipywidgets as w
    import pandas as pd
    import polars as pl
    import polars.selectors as cs
    from great_tables import GT, html, loc, style
    from ipydatagrid import DataGrid
    from IPython.display import Markdown, display

except ImportError as err:
    e = "great_tables and polars are not installed. Please install them to use this module."
    logger.warning(e)
    logger.warning(f"ImportError details: {err}")
    # Optionally, you can still raise the error if you want to halt execution:
    # raise ImportError(e) from err

import itertools
import json
import random

import yaml

from bdns_plus.abbreviations import get_asset_abbreviations
from bdns_plus.gen_idata import GenDefinition, batch_gen_idata
from bdns_plus.models import INSTANCE_REFERENCE_FSTRING, Config, ConfigIref, ITagData, TagDef, TTagData
from bdns_plus.tag import Tag

LEVEL_MIN, LEVEL_MAX, NO_VOLUMES = -1, 3, 1


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
    header = f"### {tag.name}" + "\n\n" + tag.description
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
- An enumerating integer value is added to ensure uniqueness for a given floor / level (volume_level_instance).
- These numbers are joined without delimiter to create a unique number for a given abbreviation:
  - {INSTANCE_REFERENCE_FSTRING.replace("{", "[").replace("}", "]")}"""


def markdown_callout(string: str, callout_type: str = "note", title: str = "", collapse: str = "true") -> str:
    header = "::: {.callout-" + callout_type + " " + f"collapse={collapse}" + "}"
    return f"""{header}
## {title}

{string}
:::"""


def get_idata_tag_table(idata: list[ITagData], config: Config = None) -> tuple[list[tuple[str, str]], list[dict]]:
    map_abbreviation_description = get_asset_abbreviations()
    li = []
    for x in idata:
        tag = Tag(x, config=config)

        tag_data = {
            "asset_description": map_abbreviation_description[x.abbreviation.value],
            "bdns_tag": tag.bdns,
            "type_tag": tag.type,
            "instance_tag": tag.instance,
            "is_custom": tag.is_custom,
        }
        li.append(x.model_dump(mode="json") | tag_data)

    li = [{k: v for k, v in x.items() if v is not None} for x in li]
    user_defined = [
        "abbreviation",
        "volume",
        # "type_reference",
        # "type_extra",
        "level",
        "volume_level_instance",
    ]
    generated = [
        "is_custom",
        "asset_description",
        "type_tag",
        "instance_tag",
        "bdns_tag",
    ]
    # header = [("user-defined", x) for x in user_defined] + [("generated", x) for x in generated]
    header = user_defined + generated
    return header, li


def get_electrical_distrubution_system(config_iref: ConfigIref) -> list[ITagData]:
    gf = next(x.code for x in config_iref.levels if int(x.id) == 0)  # ground floor

    gen_defs = [
        GenDefinition(abbreviation=["PB"], types=[1], no_items=1, on_levels=[gf], on_volumes=None),  # 1 pb in GF
        GenDefinition(
            abbreviation=["DB", "EM"],
            types=[1, 1],
            no_items=2,
            on_levels=None,
            on_volumes=None,
        ),  # 2 dbs / floor
        GenDefinition(
            abbreviation=["DB", "EM"],
            types=[2, 2],
            no_items=2,
            on_levels=[gf],
            on_volumes=None,
        ),  # extras on GF
        GenDefinition(
            abbreviation=["EISO"],
            types=[1],
            no_items=1,
            on_levels=None,
            on_volumes=None,
        ),  # isolator 1 per flor
    ]

    return batch_gen_idata(gen_defs, config_iref)


def get_vent_equipment(config_iref: ConfigIref) -> list[ITagData]:
    gf = next(x.code for x in config_iref.levels if int(x.id) == 0)  # ground floor
    rf = config_iref.levels[-1].code  # roof floor
    vol1 = next(x.code for x in config_iref.volumes if int(x.id) == 1)  # volume 1
    vent_equipment = batch_gen_idata(
        [
            GenDefinition(abbreviation=["AHU"], types=[1], no_items=1, on_levels=[rf], on_volumes=None),
            GenDefinition(abbreviation=["MVHR", "TEF"], types=[1, 1], no_items=1, on_levels=None, on_volumes=None),
            GenDefinition(abbreviation=["KEF"], types=[1], no_items=1, on_levels=[gf], on_volumes=[vol1]),
            GenDefinition(abbreviation=["KEF"], types=[2], no_items=1, on_levels=[rf], on_volumes=[vol1]),
        ],
        config_iref,
    )
    # add uniclass_ss for vent equipment to demo custom tags
    return [ITagData(**item.model_dump() | {"uniclass_ss": "Ss_65"}) for item in vent_equipment]


def get_electrical_accessory_types():
    """
    Generate a list of TTagData objects for predefined electrical accessories.

    Returns:
        list: A list of TTagData objects with abbreviations and type references.

    """
    abbreviations = ["DSSO", "DSO", "SSSO", "SSO", "FLRB", "INSO"]
    type_references = [4, 2, 3, 2, 3, 2]

    accessories = []
    for abbreviation, type_ref in zip(abbreviations, type_references, strict=False):
        for n in range(1, type_ref):
            accessories.append(TTagData(abbreviation=abbreviation, type_reference=n))
    return accessories


def get_light_fitting_types():
    li = ["LT", "DL", "EXIT", "PL", "SL"]

    li_nos = [3, 3, 4, 4, 2]  # [random.randint(2, 4) for n in range(0, len(li))]
    # ^ fixed random no's so git doesn't complain
    map_e = {0: "", 1: "E"}
    typs = []
    for abbreviation, type_ref in zip(li, li_nos, strict=False):
        for n in range(1, type_ref):
            e = map_e[int(1 / random.randint(1, 5))]
            if abbreviation == "EXIT":
                e = "E"
            typs.append(TTagData(abbreviation=abbreviation, type_reference=n, type_extra=e))
    return typs


def get_tags(tag_data: TTagData | ITagData, config: Config = None):
    tag = Tag(tag_data, config=config)
    if tag_data.__class__ == TTagData:
        return {
            "type_tag": tag.type,
            "is_custom": tag.is_custom,
        }
    return {
        "type_tag": tag.type,
        "instance_tag": tag.instance,
        "bdns_tag": tag.bdns,
        "is_custom": tag.is_custom,
    }


def gen_project_equipment_data(config: Config = None):
    if config is None:
        config = Config()
    di = {
        "electrical distribution": get_electrical_distrubution_system(config),
        "electrical accessories": get_electrical_accessory_types(),
        "light fittings": get_light_fitting_types(),
        "ventilation equipment": get_vent_equipment(config_iref=config),
    }

    di_ = {
        k: [{"section": k} | x.model_dump(mode="json") | get_tags(x, config=config) for x in v] for k, v in di.items()
    }

    li = list(itertools.chain.from_iterable(di_.values()))
    di_arrays = {key: [d.get(key, None) for d in li] for key in li[0]}
    di_arrays = {k: [str(x) if x is not None else "" for x in v] for k, v in di_arrays.items()}

    return pl.DataFrame(di_arrays)


def display_tag_data(df_tags):  # : pl.DataFrame -> GT
    domain = df_tags.select(pl.col("section")).unique().to_series().to_list()
    return (
        GT(df_tags)
        .tab_header(
            title="Equipment Tags",
            subtitle="Projects contain multiple identical (equipment) type_tag's. bdns_tag's and instance_tag's are unique.",
        )
        .fmt_markdown(columns=["abbreviation"])
        .cols_label_rotate(
            columns=[
                "abbreviation",
                "type_reference",
                "type_extra",
                "volume",
                "level",
                "volume_level_instance",
                "instance_extra",
                "is_custom",
            ],
        )
        .cols_hide(columns=["is_custom"])
        .tab_spanner(
            label="type inputs",
            columns=["abbreviation", "type_reference", "type_extra"],
        )
        .tab_spanner(
            label="instance inputs",
            columns=["volume", "level", "volume_level_instance", "instance_extra"],
        )
        .tab_spanner(
            label="generated outputs",
            columns=["is_custom", "type_tag", "instance_tag", "bdns_tag"],
        )
        .data_color(
            columns=["section"],
            domain=domain,
            palette="GnBu",
            na_color="white",
        )
        .tab_style(
            style.fill(color="yellow"),
            loc.body(
                columns=["type_tag", "instance_tag"],
                rows=pl.col("is_custom").str.contains("True"),
            ),
        )
        .tab_source_note(source_note="Yellow highlighting rows indicate rows that have custom tags.")
    )


def display_config_summary(config: Config):
    """Display a summary of the configuration."""
    data = config.model_dump(mode="json")
    levels, volumes, tag_bdns, tag_type, tag_instance, custom_tags = (
        pd.DataFrame.from_records(data["volumes"]).set_index("id"),
        pd.DataFrame.from_records(data["levels"]).set_index("id"),
        pd.DataFrame(data["bdns_tag"]["fields"]),
        pd.DataFrame(data["t_tag"]["fields"]),
        pd.DataFrame(data["i_tag"]["fields"]),
        data["custom_tags"],
    )
    if custom_tags is None:
        display_custom_tags = w.HTML("No custom tags defined.")
    else:
        display_custom_tags = w.HTML(
            markdown_callout(
                data_as_yaml_markdown(custom_tags),
                callout_type="info",
                title="Custom Tags",
            ),
        )

    titles = ["volumes", "levels", "tag_bdns", "tag_type", "tag_instance", "custom_tags"]
    grids = [
        DataGrid(levels, column_widths={"name": 200}),
        DataGrid(volumes, column_widths={"name": 200}),
        *(DataGrid(x, column_widths={"field_name": 150}) for x in [tag_bdns, tag_type, tag_instance]),
        display_custom_tags,
    ]
    return w.Tab(
        grids,
        titles=titles,
    )


def display_config_user_and_generated(user_input: dict, config: Config):
    out = w.Output(layout=w.Layout(width="100%"))
    with out:
        display(
            Markdown(f"""{json.dumps(user_input, indent=2)}"""),
        )

    return w.Accordion(
        [
            out,
            display_config_summary(config),
        ],
        titles=[
            "User Input Config",
            "Resultant Config Summary",
        ],
    )
