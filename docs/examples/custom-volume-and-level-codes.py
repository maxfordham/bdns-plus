# %% [markdown]
# ---
# title: custom-volume-and-level-codes
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
    gen_project_equipment_data,
    display_tag_data,
)
from bdns_plus.models import Config, Level, Volume, ConfigIref

user_input_config = {
    "volumes": [
        Volume(id=1, code="A", name="Block A").model_dump(),
        Volume(id=2, code="B", name="Block B").model_dump(),
    ],
    "levels": [
        Level(id=99, code="B1", name="Basement 1").model_dump(),
        Level(id=0, code="GF", name="Ground Floor").model_dump(),
        Level(id=1, code="L1", name="Level 1").model_dump(),
        Level(id=2, code="L2", name="Level 2").model_dump(),
    ],
}
config = Config(**user_input_config)
display_config_user_and_generated(user_input_config, config)


# %%
df = gen_project_equipment_data(config=config)
display_tag_data(df)
