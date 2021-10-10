import secrets

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from patsy.routes import auth
from patsy.settings import CONFIG, TEMPLATES

app = FastAPI(
    docs_url=None,
    redoc_url=None
)


app.include_router(auth.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "HEAD"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="patsy/static"), name="static")


def custom_openapi():
    """Creates a custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Patsy API",
        description=None,
        version=CONFIG.version,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.exception_handler(StarletteHTTPException)
async def my_exception_handler(request: Request, exception: StarletteHTTPException):
    """Custom exception handler to render template for 404 error."""
    if exception.status_code == 404:
        return TEMPLATES.TemplateResponse(
            name="not_found.html",
            context={"request": request},
            status_code=exception.status_code
        )
    return JSONResponse(
        status_code=exception.status_code,
        content={"message": exception.detail}
    )


@app.get("/", include_in_schema=False)
async def docs(request: Request):
    """Return the API docs."""
    template_name = "docs.html"
    return TEMPLATES.TemplateResponse(template_name, {"request": request})


@app.get("/ping", include_in_schema=False)
async def pingpong():
    """Basic ping/pong endpoint for ready checks."""
    return "pong!"


app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(64))
