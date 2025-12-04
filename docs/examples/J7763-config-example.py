# %% [markdown]
# ---
# title: J7716-config-example
# execute:
#   echo: false
# format:
#   html:
#     code-fold: true
# ---

# %% [markdown]
"""
Within the default configuration, the volume and level codes are simple integers.
It is possible to create project specific codes and names as shown below for volumes and levels.
"""

# %%
LEVEL_MIN, LEVEL_MAX, NO_VOLUMES = 0, 12, 2
from bdns_plus.docs import (  # noqa: E402
    display_config_user_and_generated,
    display_tag_data,
    gen_project_equipment_data,
)
from bdns_plus.models import Config, ConfigIref, Level, TagDef, TagField, Volume  # noqa: E402

user_input_config = {
    "levels": [
        {"id": 90, "code": "XX", "name": "Not Applicable"},
        {"id": 80, "code": "ZZ", "name": "Multiple Levels"},
        {"id": 91, "code": "B1", "name": "First Level of Basement"},
        {"id": 92, "code": "B2", "name": "Second Level of Basement"},
        {"id": 0, "code": "00", "name": "Level 00"},
        {"id": 1, "code": "01", "name": "Level 01"},
        {"id": 2, "code": "02", "name": "Level 02"},
        {"id": 3, "code": "03", "name": "Level 03"},
        {"id": 4, "code": "04", "name": "Level 04"},
        {"id": 5, "code": "05", "name": "Level 05"},
        {"id": 6, "code": "06", "name": "Level 06"},
        {"id": 7, "code": "07", "name": "Level 07"},
        {"id": 8, "code": "08", "name": "Level 08"},
        {"id": 9, "code": "09", "name": "Level 09"},
        {"id": 10, "code": "10", "name": "Level 10"},
        {"id": 11, "code": "11", "name": "Level 11"},
        {"id": 12, "code": "12", "name": "Level 12"},
        {"id": 81, "code": "M1", "name": "Mezzanine Above Level 01"},
        {"id": 82, "code": "M2", "name": "Mezzanine Above Level 02"},
        {"id": 71, "code": "R1", "name": "Roof Level (R1)"},
        {"id": 72, "code": "R2", "name": "Roof Level (R2)"},
        {"id": 73, "code": "R3", "name": "Roof Level (R3)"},
    ],
    "volumes": [
        {"id": 90, "code": "XX", "name": "Volume Not Applicable"},
        {"id": 80, "code": "ZZ", "name": "Multiple Zones/Sitewide"},
        {"id": 91, "code": "B1", "name": "Main Building (B1)"},
        {"id": 92, "code": "B2", "name": "25m Pool Building (B2)"},
        {"id": 93, "code": "B3", "name": "Indoor Athletics & Walkway (B3)"},
        {"id": 94, "code": "B4", "name": "Former 5-a-side & Bar (B4)"},
        {"id": 95, "code": "B5", "name": "West Stand (B5)"},
        {"id": 96, "code": "B6", "name": "Jubilee Stand (B6)"},
        {"id": 97, "code": "B7", "name": "The Lodge & Attached Ancillary Buildings (B7)"},
        {"id": 98, "code": "B8", "name": "The Houses (B8)"},
        {"id": 1, "code": "L1", "name": "Landscape Zone 1"},
        {"id": 2, "code": "L2", "name": "Landscape Zone 2"},
        {"id": 3, "code": "L3", "name": "Landscape Zone 3"},
        {"id": 4, "code": "L4", "name": "Landscape Zone 4"},
    ],
    "i_tag": {
        "name": "Instance Tag (custom)",
        "description": "Instance tag with custom fields and prefixes",
        "fields": [
            {"field_name": "abbreviation", "suffix": "/"},
            {"field_name": "volume", "suffix": "/"},
            {"field_name": "level", "suffix": "/"},
            {"field_name": "volume_level_instance", "suffix": "/", "zfill": 2},
            {"field_name": "instance_extra", "allow_none": True},
        ],
    },
    "t_tag": {
        "name": "Type Tag (dash)",
        "description": "Type tag with dash between abbreviation and type reference",
        "fields": [
            {"field_name": "abbreviation"},
            {"field_name": "type_reference", "prefix": "-"},
            {"field_name": "type_extra", "prefix": "/", "allow_none": True},
        ],
    },
}

config = Config(**user_input_config)
display_config_user_and_generated(user_input_config, config)


# %%
df = gen_project_equipment_data(config=config)
display_tag_data(df)
