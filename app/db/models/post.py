from typing import List
from sqlmodel import Field, Relationship
import uuid as uuid_pkg

from .base import UUIDModel, TimestampModel
from .post_media import PostMediaModel

class PostModel(TimestampModel, UUIDModel, table=True):
    __tablename__ = "posts"
    content: str
    like_count: int
    author_id: uuid_pkg.UUID = Field(foreign_key="users.id")
    
    posts_media: List["PostMediaModel"] = Relationship(
        sa_relationship_kwargs={
            "cascade": "delete"
        }
    )