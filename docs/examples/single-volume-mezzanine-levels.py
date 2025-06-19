# %% [markdown]
# ---
# title: single-volume-mezzanine-levels
# execute:
#   echo: false
# format:
#   html:
#     code-fold: true
# ---

# %% [markdown]
"""
::: {.callout-caution collapse="true"}
## Warning - Mezzanine Levels can lead to confusing BDNS Tags

Mezzanine levels are by definition not full levels, they are sub-levels of a main level.
This is impossible to correctly represent with an integer number, though they require an integer id to create a valid BDNS tag.
For example L1 can be represented as 1, but then M1 must be represented by the next integer number (2) meaning that L3 must be represented by 4.
This is demonstrated in the example below.
:::

"""

# %%
from bdns_plus.docs import (
    display_config_user_and_generated,
    display_tag_data,
    gen_project_equipment_data,
)
from bdns_plus.models import Config, Level, Volume

user_input_config = {
    "volumes": [Volume(id=1, code=1, name="My Building Name").model_dump()],
    "levels": [
        Level(id=99, code="B1", name="Basement 1").model_dump(),
        Level(id=0, code="GF", name="Ground Floor").model_dump(),
        Level(id=1, code="L1", name="Level 1").model_dump(),
        Level(id=2, code="M1", name="Mezzanine 1").model_dump(),
        Level(id=3, code="L2", name="Level 2").model_dump(),
    ],
}
config = Config(**user_input_config)
display_config_user_and_generated(user_input_config, config)


# %%
df = gen_project_equipment_data(config=config)
display_tag_data(df)
