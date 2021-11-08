from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from patsy.dependancies.database import get_session
from patsy.models.users import UserCreate, UserRead, UserUpdate, UsersTable

router = APIRouter(include_in_schema=True)


@router.post("/users/", response_model=UserRead)
async def create_user(*, session: AsyncSession = Depends(get_session), user: UserCreate):
    """Creates a new user."""
    db_user = UsersTable.from_orm(user)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(*, session: AsyncSession = Depends(get_session), user_id: int):
    """Get info on a single user."""
    user = await session.get(UsersTable, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", response_model=list[UserRead])
async def get_users(
    *,
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    """Get a list of all users."""
    result = await session.execute(select(UsersTable).offset(offset).limit(limit))
    users = result.scalars().all()
    return users


@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: int,
    user: UserUpdate
):
    """Updates a user."""
    db_user = await session.get(UsersTable, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user
