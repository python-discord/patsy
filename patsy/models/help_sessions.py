import datetime
from typing import Optional

from sqlmodel import BigInteger, Column, DateTime, Field, SQLModel


class HelpSessions(SQLModel, table=True):
    """A model for storing information about individual help sessions."""

    __tablename__ = "help_sessions"

    session_id: Optional[int] = Field(default=None, primary_key=True)
    claimant_id: int = Field(sa_column=BigInteger, foreign_key="users.user_id", nullable=False)
    channel_id: int = Field(sa_column=BigInteger, nullable=False, index=True)

    opened_at: datetime.datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        )
    )
    closed_at: Optional[datetime.datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True
        )
    )
