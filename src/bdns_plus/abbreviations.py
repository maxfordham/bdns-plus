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


def get_local_asset_abbreviations():
    return list(csv.reader(FPTH_LOCAL_BDNS.read_text().split("\n")))


def get_github_asset_abbreviations():
    csv_data = StringIO(requests.get(ENV.URL_ABBREVIATIONS).content.decode())
    return list(csv.reader(csv_data))


def get_bdns_asset_abbreviations():
    try:
        data = get_github_asset_abbreviations()
    except:
        logger.warning(
            "could not retrieve abbreviations from GitHub - using local copy.",
        )
        data = get_local_asset_abbreviations()
    return data


def get_bdns_asset_abbreviations_enum() -> dict[str, str]:
    return {x[1]: x[1] for x in get_bdns_asset_abbreviations()[1:]}
