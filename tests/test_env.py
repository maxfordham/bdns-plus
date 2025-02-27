import os
from bdns_plus.env import Env


def test_env():
    env = Env()
    assert (
        env.URL_ABBREVIATIONS
        == "https://raw.githubusercontent.com/theodi/BDNS/master/BDNS_Abbreviations_Register.csv"
    )


def test_env_change_version():
    os.environ["BDNS_VERSION"] = "1.4.1"
    env = Env()
    assert (
        env.URL_ABBREVIATIONS
        == "https://raw.githubusercontent.com/theodi/BDNS/1.4.1/BDNS_Abbreviations_Register.csv"
    )

    os.environ["BDNS_VERSION"] = "1.3.0"
    env.__init__()
    assert (
        env.URL_ABBREVIATIONS
        == "https://raw.githubusercontent.com/theodi/BDNS/1.3.0/BDNS_Abbreviations_Register.csv"
    )
