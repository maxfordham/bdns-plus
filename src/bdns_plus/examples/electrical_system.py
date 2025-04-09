from bdns_plus.gen_idata import batch_gen_idata, gen_config_iref
from bdns_plus.models import ConfigIref, GenDefinition



def get_electrical_system(level_min=-1, level_max=3, no_volumes=1):
    config_iref = gen_config_iref(level_min, level_max, no_volumes)
    gen_def1 = GenDefinition(abbreviation=["PB"], no_items=1, on_levels=[0], on_volumes=None)  # 1 pb in GF
    gen_def2 = GenDefinition(abbreviation=["DB", "EM"], no_items=2, on_levels=None, on_volumes=None)  # 2 dbs / floor
    gen_def3 = GenDefinition(abbreviation=["DB", "EM"], no_items=2, on_levels=[0], on_volumes=None)  # 1 pb in GF
    gen_defs = [gen_def1, gen_def2, gen_def3]

    return batch_gen_idata(gen_defs, config_iref)
