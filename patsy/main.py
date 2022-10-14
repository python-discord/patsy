from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# from patsy.routes.v1 import v1_router
from patsy.settings import CONFIG

app = FastAPI(debug=CONFIG.debug, redoc_url="/", title="Patsy API", version=CONFIG.version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "HEAD"],
    allow_headers=["*"],
)

# app.include_router(v1_router)


@app.exception_handler(StarletteHTTPException)
async def my_exception_handler(request: Request, exception: StarletteHTTPException) -> JSONResponse:
    """Custom exception handler to render template for 404 error."""
    return JSONResponse(status_code=exception.status_code, content={"message": exception.detail})


@app.get("/ping", include_in_schema=False)
async def ping_pong() -> str:
    """Basic ping/pong endpoint for ready checks."""
    return "pong!"
