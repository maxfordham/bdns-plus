# %% [markdown]
# ---
# title: no-config-single-volume
# execute:
#   echo: false
# format:
#   html:
#     code-fold: true
# ---

# %% [markdown]
"""
With no project configuration, this example generates a single volume with 4 levels.

User-input data:
"""

# %%
LEVEL_MIN, LEVEL_MAX, NO_VOLUMES = -1, 3, 1

from bdns_plus.docs import (
    display_config_user_and_generated,
    display_tag_data,
    gen_project_equipment_data,
)
from bdns_plus.models import Config, Volume

user_input_config = {
    "volumes": [Volume(id=1, code=1, name="Volume 1").model_dump()],
}
config = Config(**user_input_config)
display_config_user_and_generated(user_input_config, config)


# %%

df = gen_project_equipment_data(level_min=LEVEL_MIN, level_max=LEVEL_MAX, no_volumes=NO_VOLUMES, config=config)
display_tag_data(df)

# %%
df
