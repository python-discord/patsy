from pydantic import BaseModel, validator

from patsy.models.schemas import utils


class HelpPostMessageBase(BaseModel):
    """A message in a help post."""

    message_id: int

    # validators
    _ensure_valid_message_id = validator("message_id", allow_reuse=True)(utils.discord_ids_must_be_snowflake)

    class Config:
        """Enable instantiating this class from ORM instances."""

        orm_mode = True


class HelpPostMessagePut(HelpPostMessageBase):
    """A new message in a help post."""

    in_reply_to_message_id: int | None
    author_id: int
    post_id: int
    content: str

    # validators
    _ensure_valid_message_id = validator("in_reply_to_message_id", "author_id", "post_id", allow_reuse=True)(
        utils.discord_ids_must_be_snowflake,
    )

    @validator("in_reply_to_message_id")
    @classmethod
    def message_must_not_be_reply_to_itself(  # type: ignore[no-untyped-def]
        cls,
        value: int,
        values: dict,  # type: ignore[type-arg]
        **kwargs,
    ) -> int:
        """Ensure that the message is not a reply to itself."""
        if value == values["message_id"]:
            msg = "Message can not be a reply to itself."
            raise ValueError(msg)
        return value
