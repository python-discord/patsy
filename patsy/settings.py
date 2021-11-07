import typing as t

import tomlkit
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings


class _Config(BaseSettings):
    """General configuration settings for the service."""

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    def _get_project_version() -> str:
        with open("pyproject.toml") as pyproject:
            file_contents = pyproject.read()

        return tomlkit.parse(file_contents)["tool"]["poetry"]["version"]

    version: str = _get_project_version()
    debug: bool = False
    state_secret: str

    dev_guild_id: t.Optional[int] = None
    pydis_guild_id = 267624335836053506
    guild_id: int = dev_guild_id or pydis_guild_id


class _Database(BaseSettings):
    """Settings for the database connection."""

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    database_url: str


CONFIG: _Config = _Config()
DATABASE: _Database = _Database()
TEMPLATES: Jinja2Templates = Jinja2Templates(directory="patsy/templates")
