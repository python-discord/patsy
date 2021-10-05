import typing as t

import tomlkit
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings


class _Config(BaseSettings):
    """General configuration settings for the service."""

    def _get_project_version() -> str:
        with open("pyproject.toml") as pyproject:
            file_contents = pyproject.read()

        return tomlkit.parse(file_contents)["tool"]["poetry"]["version"]

    version: str = _get_project_version()
    debug: bool = False

    dev_guild_id: t.Optional[int] = None
    pydis_guild_id = 267624335836053506
    guild_id: int = dev_guild_id or pydis_guild_id


class _OAuthDetails(BaseSettings):
    """Discord OAuth details, loaded from env vars."""

    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: tuple[str, ...] = ("identify", "guilds")


CONFIG: _Config = _Config()
OAUTHDETAILS: _OAuthDetails = _OAuthDetails()
TEMPLATES: Jinja2Templates = Jinja2Templates(directory="patsy/templates")
