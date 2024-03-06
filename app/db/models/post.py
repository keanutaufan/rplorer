from sqlmodel import Field
import uuid as uuid_pkg

from .base import UUIDModel, TimestampModel

class PostModel(TimestampModel, UUIDModel, table=True):
    __tablename__ = "posts"
    content: str
    author_id: uuid_pkg.UUID = Field(foreign_key="users.id")