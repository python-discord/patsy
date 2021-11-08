from typing import Optional

from sqlmodel import BigInteger, Column, Field, SQLModel


class UserBase(SQLModel):
    """A base model for storing information about users."""

    opted_out: Optional[bool]


class UsersTable(UserBase, table=True):
    """A table for storing information about users."""

    __tablename__ = "users"

    user_id: int = Field(sa_column=Column("user_id", BigInteger, primary_key=True))
    opted_out: bool = Field(default=False, nullable=False)


class UserCreate(UserBase):
    """Information required to create a user."""

    user_id: int


class UserUpdate(UserBase):
    """Information required to update a user."""


class UserRead(UsersTable):
    """Information about a single user."""
