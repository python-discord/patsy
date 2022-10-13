import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String

from patsy.models.orm.base import Base


class User(Base):
    """A model for storing information about users."""

    __tablename__ = "users"

    user_id: int = Column(Integer, primary_key=True)
    opted_out: bool = Column(Boolean, default=False)


class HelpSession(Base):
    """A model for storing information about individual help sessions."""

    __tablename__ = "help_sessions"

    session_id: int = Column(Integer, primary_key=True)
    claimant_id: int = Column(ForeignKey(User.user_id))
    channel_id: int = Column(BigInteger)
    opened_at: datetime.datetime = Column(DateTime)
    closed_at: Optional[datetime.datetime] = Column(DateTime)


class Message(Base):
    """A model for storing information about messages in help sessions."""

    __tablename__ = "messages"

    message_id: int = Column(BigInteger, primary_key=True)
    author_id: int = Column(ForeignKey(User.user_id))
    session_id: int = Column(ForeignKey(HelpSession.session_id))
    channel_id: int = Column(BigInteger)
    content: str = Column(String(4000))
