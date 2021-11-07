from typing import Optional

from sqlmodel import BigInteger, Field, SQLModel


class Users(SQLModel, table=True):
    """A model for storing information about users."""

    user_id: int = Field(sa_column=BigInteger, primary_key=True)
    opted_out: Optional[bool] = Field(default=False, nullable=False)
