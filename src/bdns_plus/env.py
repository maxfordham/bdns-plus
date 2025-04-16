from __future__ import annotations

import pathlib  # noqa: TC003

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings

ABBREVIATIONS_BDNS_URL = "https://raw.githubusercontent.com/theodi/BDNS/{BDNS_VERSION}/BDNS_Abbreviations_Register.csv"
ABBREVIATIONS_BDNS_REPO_URL = "https://github.com/theodi/BDNS/blob/{BDNS_VERSION}/BDNS_Abbreviations_Register.csv"


class Env(BaseSettings):
    BDNS_VERSION: str = Field("master", description="BDNS version. Allows a project to pin to a specifc version.")
    ABBREVIATIONS_CUSTOM: pathlib.Path | None = Field(
        None,
        description="Custom abbreviations file. Allows project additions and modifications to BDNS abbreviations register.",
    )
    LEVELS: pathlib.Path | None = Field(None, description="allows user to define only levels present in the project")
    VOLUMES: pathlib.Path | None = Field(None, description="allows user to define only volumes present in the project")
    # in-place reloading possible:
    # https://docs.pydantic.dev/latest/concepts/pydantic_settings/#in-place-reloading

    @computed_field
    def ABBREVIATIONS_BDNS(self) -> str:  # noqa: D102, N802
        return ABBREVIATIONS_BDNS_URL.format(BDNS_VERSION=self.BDNS_VERSION)

    @computed_field
    def ABBREVIATIONS_BDNS_REPO(self) -> str:  # noqa: D102, N802
        return ABBREVIATIONS_BDNS_REPO_URL.format(BDNS_VERSION=self.BDNS_VERSION)
