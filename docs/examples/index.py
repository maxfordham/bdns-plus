# %% [markdown]
# ---
# title: no-config-multi-volume
# execute:
#   echo: false
# format:
#   html:
#     code-fold: true
# ---

# %% [markdown]
"""
With no project configuration levels and volumes are represented as integer numbers.
The available codes are:

- Levels -10 -> 90
- Volumes 1 -> 9

"""

# %%
LEVEL_MIN, LEVEL_MAX, NO_VOLUMES = -1, 3, 2
from bdns_plus.docs import (
    display_config_user_and_generated,
    display_tag_data,
    gen_project_equipment_data,
)
from bdns_plus.gen_idata import gen_config_iref
from bdns_plus.models import Config, Volume

user_input_config = {}
config = Config(**user_input_config)
display_config_user_and_generated(user_input_config, config)


# %%
config_iref = gen_config_iref(level_min=LEVEL_MIN, level_max=LEVEL_MAX, no_volumes=NO_VOLUMES)
config = Config(**config_iref.model_dump() | user_input_config)
df = gen_project_equipment_data(config=config)
display_tag_data(df)
