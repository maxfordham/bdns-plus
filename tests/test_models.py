from bdns_plus.gen_levels_volumes import LEVEL_MAX, LEVEL_MIN, NO_VOLUMES
from bdns_plus.models import Config


def test_config():
    config = Config()
    assert len(config.levels) == LEVEL_MAX - LEVEL_MIN + 1, "default levels found."
    assert len(config.volumes) == NO_VOLUMES, "default volumes found."
    assert config.level_no_digits == 2
    assert config.volume_no_digits == 1
    assert config.is_bdns_plus_default

    if config.no_volumes == 1:
        assert "volume" not in [x.field_name for x in config.i_tag.fields]


def test_pycountry():
    import pycountry

    germany = pycountry.countries.get(alpha_2="DE")
    assert germany.name == "Germany"
    test = pycountry.countries.get(alpha_2="ASDF")
    assert test is None
