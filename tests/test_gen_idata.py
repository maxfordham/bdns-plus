from bdns_plus.gen_idata import batch_gen_idata, gen_config_iref, gen_idata
from bdns_plus.models import GenDefinition


def get_config_iref():
    level_min, level_max, no_volumes = -1, 3, 1
    return gen_config_iref(level_min, level_max, no_volumes)


def get_electrical_system():
    config_iref = get_config_iref()
    gen_def1 = GenDefinition(abbreviation=["PB"], no_items=1, on_levels=[0], on_volumes=None)  # 1 pb in GF
    gen_def2 = GenDefinition(abbreviation=["DB", "EM"], no_items=2, on_levels=None, on_volumes=None)  # 2 dbs / floor
    gen_def3 = GenDefinition(abbreviation=["DB", "EM"], no_items=2, on_levels=[0], on_volumes=None)  # 1 pb in GF
    gen_defs = [gen_def1, gen_def2, gen_def3]

    return batch_gen_idata(gen_defs, config_iref)


def test_gen_config_iref():
    level_min, level_max, no_volumes = -1, 3, 1

    config_iref = gen_config_iref(level_min, level_max, no_volumes)
    assert len(config_iref.levels) == 5
    assert len(config_iref.volumes) == 1


def test_gen_idata():
    config_iref = get_config_iref()
    gen_def = GenDefinition(abbreviation="DB", no_items=2, on_levels=None, on_volumes=None)
    result = gen_idata(gen_def, config_iref)

    assert len(result) == 10


def test_batch_gen_idata():
    result = get_electrical_system()
    assert {"DB", "EM", "PB"} == {x.abbreviation.value for x in result}
