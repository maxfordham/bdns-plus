from bdns_plus.config import gen_config_package, gen_levels_resource, gen_volumes_resource
from bdns_plus.gen_levels_volumes import LEVEL_MAX, LEVEL_MIN, NO_VOLUMES


def test_gen_levels_resource():
    res = gen_levels_resource()
    assert res.header == ["id", "code", "name"]
    assert len(res.read_rows()) == LEVEL_MAX - LEVEL_MIN + 1, "default levels found."


def test_gen_volume_resource():
    res = gen_volumes_resource()
    assert res.header == ["id", "code", "name"]
    assert len(res.read_rows()) == NO_VOLUMES


def test_gen_config_package():
    pkg = gen_config_package()
    assert len(pkg.resources) == 2
    assert pkg.name == "bdns-plus"
    assert pkg.resources[0].name == "levels"
    assert pkg.resources[1].name == "volumes"
