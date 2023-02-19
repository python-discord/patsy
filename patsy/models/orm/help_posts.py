import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from patsy.models.orm.base import Base


class User(Base):
    """A model for storing information about users."""

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    opted_out: Mapped[bool] = mapped_column(default=False)


class HelpPost(Base):
    """A model for storing information about individual help posts."""

    __tablename__ = "help_posts"

    post_id: Mapped[int] = mapped_column(primary_key=True)
    claimant_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    opened_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    closed_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))


class Message(Base):
    """A model for storing information about messages in help posts."""

    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(primary_key=True)
    in_reply_to_message_id: Mapped[int] = mapped_column(ForeignKey("messages.message_id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("help_posts.post_id"))
    content: Mapped[str] = mapped_column(String(4000))
