# %% [markdown]
# ---
# title: custom-nomenclature-for-vent-equipment
# execute:
#   echo: false
# format:
#   html:
#     code-fold: true
# ---

# %% [markdown]
"""
This is an example from the wild, where the engineers designing the ventilation
equipment followed a different convention used elsewhere in the project. Whilst this
is generally discouraged, it is sometimes necessary to accommodate such requirements.
"""

# %%

from pyrulefilter import OperatorsEnum, Rule, RuleSet

from bdns_plus.default_fields import (
    abbreviation_field,
    instance_extra_field,
    level_field,
    level_instance_field,
    volume_field,
)
from bdns_plus.docs import (
    display_config_user_and_generated,
    display_tag_data,
    gen_project_equipment_data,
)
from bdns_plus.gen_idata import gen_config_iref
from bdns_plus.models import Config, CustomTagDef, TagDef, TagField

LEVEL_MIN, LEVEL_MAX, NO_VOLUMES = -1, 3, 2
# define tag
fields = [
    abbreviation_field(suffix="."),
    volume_field(suffix="."),
    level_field(suffix=".", zfill=2),
    level_instance_field(suffix=".", zfill=2),
    instance_extra_field(),
]
itag_def = TagDef(
    name="Custom Tags for Ventilation Equipment",
    description="ventilation contractor for xxx project required this format...",
    fields=fields,
)

# define scope of tag
r = Rule(
    parameter="uniclass_ss",
    operator=OperatorsEnum.BeginsWith,
    value="Ss_65",
)
rule_set = RuleSet(rule=[r], set_type="OR")

# define custom tag to be applied in scope
custom_tag = CustomTagDef(
    description="Custom AHU Tag",
    i_tag=itag_def,
    scope=rule_set,
)
user_input_config = {
    "custom_tags": [custom_tag.model_dump()],
}


config = Config(**user_input_config)
display_config_user_and_generated(user_input_config, config)


# %%
config_iref = gen_config_iref(level_min=LEVEL_MIN, level_max=LEVEL_MAX, no_volumes=NO_VOLUMES)
config = Config(**config_iref.model_dump() | user_input_config)
df = gen_project_equipment_data(config=config)
display_tag_data(df)

# %%
