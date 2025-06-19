from bdns_plus.docs import get_vent_equipment
from bdns_plus.gen_idata import gen_config_iref


def test_get_vent_equipment():
    config_iref = gen_config_iref(level_min=-1, level_max=3, no_volumes=1)

    vent_equipment = get_vent_equipment(config_iref)
    assert vent_equipment is not None, "Ventilation equipment data should not be None"
    assert len(vent_equipment) > 0, "Ventilation equipment data should not be empty"
