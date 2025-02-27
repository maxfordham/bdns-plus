from bdns_plus.config import gen_config_package, gen_levels, gen_levels_resource, gen_volumes_resource


def test_gen_levels():
    levels = gen_levels()
    assert len(levels) == 100


def test_gen_levels_resource():
    res = gen_levels_resource()
    assert res.header == ["level", "level_id", "level_name"]
    assert len(res.read_rows()) == 100


def test_gen_volume_resource():
    res = gen_volumes_resource()
    assert res.header == ["volume", "volume_id", "volume_name"]
    assert len(res.read_rows()) == 9


def test_gen_config_package():
    pkg = gen_config_package()
    assert len(pkg.resources) == 2
    assert pkg.name == "bdns-plus"
    assert pkg.resources[0].name == "levels"
    assert pkg.resources[1].name == "volumes"
