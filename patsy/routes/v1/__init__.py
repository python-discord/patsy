from fastapi import APIRouter, Depends

from patsy.auth import verify_token
from patsy.routes.v1.messages import message_router
from patsy.routes.v1.posts import post_router

v1_router = APIRouter(prefix="/v1/api", dependencies=[Depends(verify_token)])
v1_router.include_router(message_router)
v1_router.include_router(post_router)
