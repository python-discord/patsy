from typing import TYPE_CHECKING

from fastapi import APIRouter, Request
from sqlalchemy import exists, func, select

from patsy.models import orm, schemas

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

post_router = APIRouter(prefix="/posts")


@post_router.get("")
async def get_all_posts(
    request: Request,
    *,
    only_open_posts: bool = True,
) -> list[schemas.posts.HelpPost]:
    """
    Query all posts stored in Patsy.

    only_open_posts filters the posts returned.
    """
    session: AsyncSession = request.state.db_session
    stmt = select(orm.HelpPost)

    if only_open_posts:
        stmt = stmt.where(orm.HelpPost.closed_at is None or orm.HelpPost.closed_at < func.now())

    return list(await session.scalars(stmt))


@post_router.put("")
async def put_new_post(
    request: Request,
    help_post: schemas.posts.HelpPost,
) -> schemas.posts.HelpPost:
    """Put a new HelpPost into Patsy."""
    session: AsyncSession = request.state.db_session
    stmt = exists(orm.User.user_id).where(orm.User.user_id == help_post.claimant_id).select()
    user_exists = await session.scalar(stmt)
    if not user_exists:
        db_user = orm.User(user_id=help_post.claimant_id)
        session.add(db_user)

    db_help_post = orm.HelpPost(**help_post.dict())
    session.add(db_help_post)

    return db_help_post
