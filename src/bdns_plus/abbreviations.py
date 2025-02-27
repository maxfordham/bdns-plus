import csv
import logging
from enum import Enum
from io import StringIO

import requests

from bdns_plus.env import Env

logger = logging.getLogger(__name__)
ENV = Env()


class StrEnum(str, Enum):
    pass


def get_bdns_asset_abbreviations():
    # try:  #  read from github
    #     csv_data = StringIO(requests.get(ENV.URL_ABBREVIATIONS).content.decode())
    # except:
    #     from aectemplater_schemas.constants import FPTH_LOCAL_BDNS

    #     logger.warning(
    #         "could not retrieve abbreviations from GitHub - using local copy."
    #     )
    #     csv_data = FPTH_LOCAL_BDNS.read_text()[:-1].split("\n")
    csv_data = StringIO(requests.get(ENV.URL_ABBREVIATIONS, timeout=10).content.decode())
    return list(csv.reader(csv_data))


def get_local_asset_abbreviations():
    pass


def get_bdns_asset_abbreviations_enum() -> dict[str, str]:
    return {x[1]: x[1] for x in get_bdns_asset_abbreviations()[1:]}


AbbreviationsEnum = StrEnum("AbbreviationsEnum", get_bdns_asset_abbreviations_enum())
