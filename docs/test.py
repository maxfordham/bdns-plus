# %% [markdown]
# ---
# title: test
# format:
#   html:
#     code-fold: true
# ---

# %%
import ipywidgets as w
import pandas as pd
from ipydatagrid import DataGrid
from IPython.display import display

from bdns_plus.models import Config

config = Config()
data = config.model_dump(mode="json")
levels, volumes, tag_bdns, tag_type, tag_instance = (
    pd.DataFrame.from_records(data["levels"]),
    pd.DataFrame.from_records(data["volumes"]),
    pd.DataFrame(data["bdns_tag"]["fields"]),
    pd.DataFrame(data["t_tag"]["fields"]),
    pd.DataFrame(data["i_tag"]["fields"]),
)

titles = ["levels", "volumes", "tag_bdns", "tag_type", "tag_instance"]
grids = [
    DataGrid(levels, column_widths={"name": 200}),
    DataGrid(volumes, column_widths={"name": 200}),
    *(DataGrid(x, column_widths={"field_name": 150}) for x in [tag_bdns, tag_type, tag_instance]),
]
w.Tab(
    grids,
    titles=titles,
)
