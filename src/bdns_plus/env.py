from __future__ import annotations

import pathlib  # noqa: TC003
import typing as ty

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings


class Env(BaseSettings):
    BDNS_VERSION: str = Field("master", description="BDNS version")
    ABBREVIATIONS_BDNS: str = Field(
        "https://raw.githubusercontent.com/theodi/BDNS/{BDNS_VERSION}/BDNS_Abbreviations_Register.csv",
        description="URL to abbreviations registry",
    )
    ABBREVIATIONS_BDNS_REPO: str = Field(
        "https://github.com/theodi/BDNS/blob/{BDNS_VERSION}/BDNS_Abbreviations_Register.csv",
        description="URL to abbreviations registry for user error explanation",
    )
    ABBREVIATIONS_CUSTOM: pathlib.Path | None = Field(None, description="Custom abbreviations file")
    LEVELS: pathlib.Path | None = None
    VOLUMES: pathlib.Path | None = None
    # in-place reloading possible:
    # https://docs.pydantic.dev/latest/concepts/pydantic_settings/#in-place-reloading

    @model_validator(mode="after")
    def _build_urls(self) -> ty.Self:
        self.ABBREVIATIONS_BDNS = self.ABBREVIATIONS_BDNS.format(BDNS_VERSION=self.BDNS_VERSION)
        self.ABBREVIATIONS_BDNS_REPO = self.ABBREVIATIONS_BDNS_REPO.format(BDNS_VERSION=self.BDNS_VERSION)
        return self
