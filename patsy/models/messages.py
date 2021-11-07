from typing import Optional

from sqlmodel import BigInteger, Field, SQLModel


class Messages(SQLModel, table=True):
    """A model for storing information about individual messages."""

    message_id: Optional[int] = Field(sa_column=BigInteger, primary_key=True)
    author_id: int = Field(sa_column=BigInteger, foreign_key="users.user_id", nullable=False)
    session_id: int = Field(sa_column=BigInteger, foreign_key="help_sessions.session_id", nullable=False)
    content: str = Field(nullable=False, max_length=4000)
