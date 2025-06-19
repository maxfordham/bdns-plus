# %% [markdown]
# ---
# title: single-volume
# execute:
#   echo: false
# format:
#   html:
#     code-fold: true
# ---

# %% [markdown]
"""
When a project configuration defines only a single volume, the volume number is automatically
omitted from the instance tag.
"""

# %%
LEVEL_MIN, LEVEL_MAX, NO_VOLUMES = -1, 3, 1

from bdns_plus.docs import (
    display_config_user_and_generated,
    display_tag_data,
    gen_project_equipment_data,
)
from bdns_plus.gen_idata import gen_config_iref
from bdns_plus.models import Config, ConfigIref, Volume

user_input_config = {
    "volumes": [Volume(id=1, code=1, name="Volume 1").model_dump()],
}
config = Config(**user_input_config)
display_config_user_and_generated(user_input_config, config)


# %%
config_iref = gen_config_iref(level_min=LEVEL_MIN, level_max=LEVEL_MAX, no_volumes=NO_VOLUMES)
config = Config(**config_iref.model_dump())
df = gen_project_equipment_data(config=config)
display_tag_data(df)
