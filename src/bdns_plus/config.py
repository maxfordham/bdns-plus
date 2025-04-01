"""default configuration for bdns_plus is as follows:

- level ground and above are 2-digit zero-padded integers up to a max of 89
- level basement 1 and below are 2-digit integers 99 - 90
- the volume is a single digit integer 1 - 9
"""

from frictionless import Package
from frictionless.resources import TableResource

from .gen_levels_volumes import gen_levels_config, gen_volumes_config


def gen_levels_resource():
    data = gen_levels_config()
    res = TableResource(name="levels", data=data)
    res.read_rows()
    return res


def gen_volumes_resource():
    data = gen_volumes_config()
    res = TableResource(name="volumes", data=data)
    res.read_rows()
    return res


def gen_config_package():
    res_levels = gen_levels_resource()
    res_volumes = gen_volumes_resource()

    pkg = Package(
        name="bdns-plus",
        resources=[res_levels, res_volumes],
    )
    return pkg
