from fastapi import HTTPException, Request
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from patsy.settings import CONFIG


async def verify_token(request: Request) -> None:
    """Ensure the request contains the SECRET_KEY as a Bearer token."""
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Improper authorization",
        )
    if param != CONFIG.secret_key.get_secret_value():
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials",
        )
