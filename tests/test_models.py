from bdns_plus.models import Config

MAX_LEVELS = 100
MAX_VOLUMES = 9

def test_config():
    config = Config()
    assert len(config.levels) == MAX_LEVELS, "default levels found."
    assert len(config.volumes) == MAX_VOLUMES, "default volumes found."
    assert config.level_no_digits == 2
    assert config.volume_no_digits == 1
    assert config.is_bdns_plus_default

def test_pycountry():
    import pycountry
    germany = pycountry.countries.get(alpha_2='DE')
    assert germany.name == "Germany"
    test = pycountry.countries.get(alpha_2='ASDF')
    assert test is None