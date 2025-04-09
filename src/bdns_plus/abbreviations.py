"""load asset abbreviations from github and local file."""

import csv
import logging
from enum import Enum
from importlib.resources import files
from io import StringIO

import requests

from bdns_plus.env import Env

logger = logging.getLogger(__name__)
ENV = Env()
FPTH_LOCAL_BDNS = files("bdns_plus.data").joinpath("BDNS_Abbreviations_Register.csv")


class StrEnum(str, Enum):
    pass


def read_csv(path):
    return list(csv.reader(path.read_text().split("\n")))


def get_local_bdns_asset_abbreviations():
    return read_csv(FPTH_LOCAL_BDNS)


def get_github_bdns_asset_abbreviations():
    csv_data = StringIO(requests.get(ENV.ABBREVIATIONS_BDNS).content.decode())
    return list(csv.reader(csv_data))


def get_bdns_asset_abbreviations():
    try:
        data = get_github_bdns_asset_abbreviations()
    except:
        logger.warning(
            "could not retrieve abbreviations from GitHub - using local copy.",
        )
        data = get_local_bdns_asset_abbreviations()
    return data


def get_custom_asset_abbreviations() -> list[list]:
    return read_csv(ENV.ABBREVIATIONS_CUSTOM) if ENV.ABBREVIATIONS_CUSTOM else []


def get_asset_abbreviations() -> dict:
    bdns = {x[1]: x[0] for x in get_bdns_asset_abbreviations()[1:]}
    custom = {x[1]: x[0] for x in get_custom_asset_abbreviations()[1:]}
    return bdns | custom


def get_asset_abbreviations_enum() -> dict[str, str]:
    return {x: x for x in list(get_asset_abbreviations().keys())}
