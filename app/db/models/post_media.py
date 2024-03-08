from sqlmodel import Field
import uuid as uuid_pkg

from .base import TimestampModel

class PostMediaModel(TimestampModel, table=True):
    __tablename__ = "posts_media"
    post_id: uuid_pkg.UUID = Field(foreign_key="posts.id", primary_key=True)
    media_id: uuid_pkg.UUID = Field(foreign_key="media.id", primary_key=True)