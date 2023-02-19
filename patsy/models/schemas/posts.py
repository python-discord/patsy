import datetime

from pydantic import BaseModel, validator

from patsy.models.schemas import utils


class HelpPost(BaseModel):
    """A Discord user."""

    post_id: int
    claimant_id: int
    opened_at: datetime.datetime
    closed_at: datetime.datetime | None

    # validators
    _ensure_valid_ids = validator("post_id", "claimant_id", allow_reuse=True)(utils.discord_ids_must_be_snowflake)

    class Config:
        """Enable instantiating this class from ORM instances."""

        orm_mode = True
