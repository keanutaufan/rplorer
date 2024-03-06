from sqlmodel import Field

from .base import UUIDModel, TimestampModel

class UserModel(TimestampModel, UUIDModel, table=True):
    __tablename__ = "users"

    username: str = Field(
        index=True,
        unique=True,
        nullable=False,
    )

    display_name: str
    secret: str
    bio: str | None = None