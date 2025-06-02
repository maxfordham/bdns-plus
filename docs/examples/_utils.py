import pandas as pd

from bdns_plus.abbreviations import get_asset_abbreviations
from bdns_plus.models import Config, ITagData
from bdns_plus.tag import Tag


def get_idata_tag_table(idata: list[ITagData], config: Config = None) -> pd.DataFrame:
    map_abbreviation_description = get_asset_abbreviations()
    li = []
    for x in idata:
        tag = Tag(x, config=config)

        tag_data = {
            "asset_description": map_abbreviation_description[x.abbreviation.value],
            "bdns": tag.bdns,
            "type": tag.type,
            "instance": tag.instance,
        }
        li.append(x.model_dump(mode="json") | tag_data)

    li = [{k: v for k, v in x.items() if v is not None} for x in li]
    user_defined = [
        "abbreviation",
        # "type_reference",
        # "type_extra",
        "level",
        "level_iref",
        "volume",
    ]
    generated = [
        "asset_description",
        "bdns_tag",
        "type_tag",
        "instance_tag",
    ]
    annotated_cols = pd.MultiIndex.from_tuples(
        [("user-defined", x) for x in user_defined] + [("generated", x) for x in generated],
    )
    df = pd.DataFrame(li).sort_values(by=["level"])
    df.columns = annotated_cols
    return df
