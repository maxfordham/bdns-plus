import pytest

from bdns_plus.gen_levels_volumes import gen_levels, gen_levels_config_string_code, gen_volumes_config


def test_gen_levels():
    levels = gen_levels()
    assert len(levels) == 100


@pytest.mark.parametrize(
    ("level_min", "level_max"),
    [
        (-2, 5),
        (0, 0),
        (1, 3),
        (-5, -1),
    ],
)
def test_gen_levels_config_string_code(level_min: int, level_max: int):
    gen_levels = gen_levels_config_string_code(level_min=level_min, level_max=level_max)
    assert len(gen_levels) == level_max - level_min + 2


@pytest.mark.parametrize(
    "no_volumes",
    [1, 5, 9],
)
def test_gen_volumes_config(no_volumes: int):
    gen_volumes = gen_volumes_config(no_volumes=no_volumes)
    assert len(gen_volumes) == no_volumes + 1
