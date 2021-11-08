import datetime
from typing import Optional

from sqlmodel import BigInteger, Column, DateTime, Field, ForeignKey, SQLModel


class HelpSessionBase(SQLModel):
    """A base model for storing information about users."""

    claimant_id: int
    channel_id: int
    opened_at: datetime.datetime
    closed_at: Optional[datetime.datetime]


class HelpSessionTable(HelpSessionBase, table=True):
    """A model for storing information about individual help sessions."""

    __tablename__ = "help_sessions"

    session_id: int = Field(primary_key=True)
    claimant_id: int = Field(
        sa_column=Column(
            "claimant_id",
            BigInteger,
            ForeignKey("users.user_id"),
            nullable=False
        )
    )
    channel_id: int = Field(
        sa_column=Column(
            "channel_id",
            BigInteger,
            index=True,
            nullable=False
        )
    )
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
