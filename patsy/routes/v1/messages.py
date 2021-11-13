from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from patsy.dependancies.database import get_session
from patsy.models.messages import MessagePost, MessageRead, MessageUpdate, MessagesTable

router = APIRouter(include_in_schema=True, tags=["messages"])


@router.post("/messages/", response_model=MessageRead)
async def store_message(*, session: AsyncSession = Depends(get_session), message: MessagePost):
    """Stores the given message if the user is not opted out."""
    author = await session.get(MessagesTable, message.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")
    elif author.opt_out:
        raise HTTPException(status_code=422, detail="Author is opted out.")

    db_message = MessagesTable.from_orm(message)
    session.add(db_message)
    await session.commit()
    await session.refresh(db_message)
    return db_message


@router.get("/messages/{message_id}", response_model=MessageRead)
async def get_message(*, session: AsyncSession = Depends(get_session), message_id: int):
    """Get info on a single message."""
    message = await session.get(MessagesTable, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found.")
    return message


@router.get("/messages/", response_model=list[MessageRead])
async def get_messages(
    *,
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=1000),
):
    """Get a list of all messages."""
    result = await session.execute(select(MessagesTable).offset(offset).limit(limit))
    messages = result.scalars().all()
    return messages


@router.patch("/messages/{message_id}", response_model=MessageRead)
async def update_message(
    *,
    session: AsyncSession = Depends(get_session),
    message_id: int,
    message: MessageUpdate
):
    """Updates a message."""
    db_message = await session.get(MessagesTable, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found.")

    message_data = message.dict(exclude_unset=True)
    for key, value in message_data.items():
        setattr(db_message, key, value)
    session.add(db_message)
    await session.commit()
    await session.refresh(db_message)
    return db_message


@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    *,
    session: AsyncSession = Depends(get_session),
    message_id: int
):
    """Deletes a message."""
    db_message = await session.get(MessagesTable, message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found.")

    session.delete(db_message)
    await session.commit()
