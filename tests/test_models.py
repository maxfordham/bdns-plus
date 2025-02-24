from bdns_plus.models import Config
from typing import Annotated

def test_config():
    config = Config()
    assert len(config.levels) == 100
    assert len(config.volumes) == 9
    assert config.level_no_digits == 2
    assert config.volume_no_digits == 1

# def test_country_validator():
#     value = "EN"
#     from pydantic_extra_types.country import CountryAlpha2
#     # EvenNumber = Annotated[int, AfterValidator(is_even)]
#     check = CountryAlpha2(value)
#     assert check

#     value = "ASDF"
#     from pydantic_extra_types.country import CountryAlpha2
#     # EvenNumber = Annotated[int, AfterValidator(is_even)]
#     check = CountryAlpha2(value)
#     assert not check



def test_pycountry():
    import pycountry
    germany = pycountry.countries.get(alpha_2='DE')
    assert germany.name == "Germany"
    test = pycountry.countries.get(alpha_2='ASDF')
    assert test is None