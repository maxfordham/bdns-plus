import pandas as pd


def get_idata_tag_df(header: list[tuple], idata: list[dict]) -> pd.DataFrame:
    annotated_cols = pd.MultiIndex.from_tuples(header)
    df_tags = pd.DataFrame(idata).sort_values(by=["level"]).reset_index(drop=True)
    df_tags.columns = annotated_cols
    return df_tags
