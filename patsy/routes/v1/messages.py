from typing import TYPE_CHECKING

from fastapi import APIRouter, Request
from sqlalchemy import func, select

from patsy.models import orm, schemas

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

message_router = APIRouter(prefix="/messages")


@message_router.put("")
async def put_new_message(
    request: Request,
    message: schemas.messages.HelpPostMessagePut,  # noqa: ARG001
    *,
    only_open_posts: bool = True,
) -> list[schemas.messages.HelpPostMessagePut]:
    """
    Put a new message to Patsy.

    Create a new HelpPost if one does not already exist for the message being put.
    """
    session: AsyncSession = request.state.db_session
    stmt = select(orm.HelpPost)

    if only_open_posts:
        stmt = stmt.where(orm.HelpPost.closed_at is None or orm.HelpPost.closed_at < func.now())

    return list(await session.scalars(stmt))
