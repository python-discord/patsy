from sqlmodel import BigInteger, Column, Field, ForeignKey, SQLModel


class MessageBase(SQLModel):
    """A base model for storing information about messages."""

    content: str


class MessagesTable(MessageBase, table=True):
    """A model for storing information about individual messages."""

    __tablename__ = "messages"

    message_id: int = Field(
        sa_column=Column(
            "message_id",
            BigInteger,
            primary_key=True
        )
    )
    author_id: int = Field(
        sa_column=Column(
            "author_id",
            BigInteger,
            ForeignKey("users.user_id"),
            nullable=False
        )
    )
    session_id: int = Field(
        sa_column=Column(
            "session_id",
            BigInteger,
            ForeignKey("help_sessions.session_id"),
            nullable=False,
            index=True
        )
    )
    channel_id: int = Field(
        sa_column=Column(
            "channel_id",
            BigInteger,
            nullable=True,
            index=True
        )
    )
    content: str = Field(nullable=False, max_length=4000)


class MessagePost(MessageBase):
    """Information required to create a message."""

    message_id: int
    author_id: int
    channel_id: int


class MessageUpdate(MessageBase):
    """Information required to update a message."""


class MessageRead(MessagesTable):
    """Information about a single message."""
