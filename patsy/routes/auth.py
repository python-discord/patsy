import secrets

from fastapi import APIRouter, Cookie
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette_discord.client import DiscordOAuthClient

from patsy import logger
from patsy.settings import CONFIG, OAUTHDETAILS, TEMPLATES

router = APIRouter(include_in_schema=False)
client = DiscordOAuthClient(
    OAUTHDETAILS.client_id,
    OAUTHDETAILS.client_secret,
    OAUTHDETAILS.redirect_uri,
    OAUTHDETAILS.scopes
)


@router.get("/authorize")
async def login_with_discord(request: Request):
    """
    Redirect the user to the Discord OAuth2 flow.

    Inject a state secret into the session to ensure users hitting /callback actually came from here.
    """
    state = secrets.token_urlsafe(32)
    request.session["state"] = state
    return client.redirect(state=state, prompt="consent")


def is_guild_we_want(guild: dict) -> bool:
    """True when the given guild has an id item with the same id as from our settings."""
    try:
        id = int(guild["id"])
    except KeyError:
        logger.debug("No id element found in the guild dict!")
    except TypeError:
        logger.debug("Could not convert given guild id to an int")
    else:
        if id == CONFIG.guild_id:
            return True
    return False


@router.get("/callback")
async def callback(request: Request, code: str, state: str):
    """Fetch data about the user after authorized in Discord."""
    # Raise 401-Unauthorized if state doesn't match.
    if not state == request.session.get("state"):
        raise HTTPException(401)

    async with client.session(code) as session:
        user = await session.identify()  # noqa: F841 XXX This will be used for generating token eventually.
        guilds = await session.guilds()

    is_admin = False

    try:
        guild_info = next(filter(is_guild_we_want, guilds))
    except StopIteration:
        logger.debug("User authorizing wasn't part of the guild we care about")
    else:
        try:
            is_admin = (int(guild_info["permissions"]) & 0x4) == 0x4
        except KeyError:
            logger.debug("No permission item was found in the guild dict!")
        except TypeError:
            logger.debug("Could not convert the permission string to an int")

    # Redirect so that a user doesn't refresh the page and spam discord
    redirect = RedirectResponse("/show_token", status_code=303)
    redirect.set_cookie(
        key='token',
        value=is_admin,
        httponly=True,
        max_age=10,
        path='/show_token',
    )
    return redirect


@router.get("/show_token")
async def show_token(request: Request, token: str = Cookie(None)):  # noqa: B008
    """Show the token from the cookie to the user."""
    template_name = "cookie_disabled.html"
    context = {"request": request}

    if token:
        context["token"] = f"{token = }"
        template_name = "api_token.html"

    return TEMPLATES.TemplateResponse(template_name, context)
