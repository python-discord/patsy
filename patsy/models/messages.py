from sqlmodel import BigInteger, Column, Field, ForeignKey, SQLModel


class MessageBase(SQLModel):
    """A base model for storing information about messages."""

    author_id: int
    session_id: int
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
            nullable=False
        )
    )
    content: str = Field(nullable=False, max_length=4000)
