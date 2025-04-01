from __future__ import annotations

import pathlib  # noqa: TC003
import typing as ty

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings


class Env(BaseSettings):
    BDNS_VERSION: str = Field("master", description="BDNS version")
    URL_ABBREVIATIONS: str = Field(
        "https://raw.githubusercontent.com/theodi/BDNS/{BDNS_VERSION}/BDNS_Abbreviations_Register.csv",
        description="URL to abbreviations registry",
    )
    URL_ABBREVIATIONS_FOR_USER: str = Field(
        "https://github.com/theodi/BDNS/blob/{BDNS_VERSION}/BDNS_Abbreviations_Register.csv",
        description="URL to abbreviations registry for user error explanation",
    )
    CUSTOM_ABBREVIATIONS: pathlib.Path | None = Field(None, description="Custom abbreviations file")
    BDNS_PLUS_CONFIG_DIR: pathlib.Path | None = Field(None)
    # in-place reloading possible:
    # https://docs.pydantic.dev/latest/concepts/pydantic_settings/#in-place-reloading

    @model_validator(mode="after")
    def _build_urls(self) -> ty.Self:
        self.URL_ABBREVIATIONS = self.URL_ABBREVIATIONS.format(BDNS_VERSION=self.BDNS_VERSION)
        self.URL_ABBREVIATIONS_FOR_USER = self.URL_ABBREVIATIONS_FOR_USER.format(BDNS_VERSION=self.BDNS_VERSION)
        return self
