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
With no project configuration, this example generates a 2no volume with 4no levels.
"""

# %%
LEVEL_MIN, LEVEL_MAX, NO_VOLUMES = -1, 3, 2
from bdns_plus.docs import (
    display_config_user_and_generated,
    display_tag_data,
    gen_project_equipment_data,
)
from bdns_plus.models import Config, Volume

user_input_config = {}
config = Config(**user_input_config)
display_config_user_and_generated(user_input_config, config)


# %%
config = Config()
df = gen_project_equipment_data(level_min=LEVEL_MIN, level_max=LEVEL_MAX, no_volumes=NO_VOLUMES, config=config)
display_tag_data(df)
