import logging
import sys
import tomllib
import typing
from collections.abc import Sequence
from pathlib import Path

import pydantic
from pydantic.error_wrappers import ErrorWrapper
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

logger = logging.getLogger(__name__)

# This is available in pydantic as pydantic.error_wrappers.ErrorList
# but is typehinted as a Sequence[any], due to being a recursive type.
# This makes it harder to handle the types.
# For our purposes, a fully accurate representation is not necessary.
_PYDANTIC_ERROR_TYPE = Sequence[ErrorWrapper | Sequence[ErrorWrapper]]


class PatsyBaseSettings(pydantic.BaseSettings):
    """Base class for settings with .env support and nicer error messages."""

    @staticmethod
    def __log_missing_errors(base_error: pydantic.ValidationError, errors: _PYDANTIC_ERROR_TYPE) -> bool:
        """
        Log out a nice representation for missing environment variables.

        Returns false if none of the errors were caused by missing variables.
        """
        found_relevant_errors = False
        for error in errors:
            if isinstance(error, Sequence):
                found_relevant_errors = (
                    PatsyBaseSettings.__log_missing_errors(base_error, error) or found_relevant_errors
                )
            elif isinstance(error.exc, pydantic.MissingError):
                logger.error(
                    "Missing environment variable %s.%s",
                    base_error.args[1].__name__,
                    error.loc_tuple()[0],
                )
                found_relevant_errors = True

        return found_relevant_errors

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:  # noqa: ANN401
        """Try to instantiate the class, and print a nicer message for unset variables."""
        try:
            super().__init__(*args, **kwargs)
        except pydantic.ValidationError as error:
            if PatsyBaseSettings.__log_missing_errors(error, error.raw_errors):
                sys.exit(1)
            else:
                # The validation error is not due to an unset environment variable, propagate the error as normal
                raise error from None

    class Config:
        """Enable env files."""

        frozen = True

        env_file = ".env"
        env_file_encoding = "utf-8"


class _Config(PatsyBaseSettings):
    """General configuration settings for the service."""

    @staticmethod
    def _get_project_version() -> str:
        with Path("pyproject.toml").open("rb") as pyproject:
            file_contents = tomllib.load(pyproject)

        return file_contents["tool"]["poetry"]["version"]  # type: ignore[no-any-return]

    version: str = _get_project_version()
    debug: bool = False
    secret_key: pydantic.SecretStr

    dev_guild_id: int | None = None
    pydis_guild_id = 267624335836053506
    guild_id: int = dev_guild_id or pydis_guild_id


CONFIG: _Config = _Config()


class _ConnectionURLs(PatsyBaseSettings):
    """Settings for the database connection."""

    DATABASE_URL: pydantic.SecretStr


ConnectionURLs = _ConnectionURLs()


class Connections:
    """How to connect to other, internal services."""

    DB_ENGINE = create_async_engine(ConnectionURLs.DATABASE_URL.get_secret_value())
    DB_SESSION = async_sessionmaker(DB_ENGINE)
