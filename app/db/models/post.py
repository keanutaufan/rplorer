from sqlmodel import Field
import uuid as uuid_pkg

from .base import UUIDModel, TimestampModel

class PostModel(TimestampModel, UUIDModel):
    __tablename__ = "posts"
    content: str
    author_id: uuid_pkg.uuid4 = Field(foreign_key="users.id")