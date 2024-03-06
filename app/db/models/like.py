from sqlmodel import Field
import uuid as uuid_pkg

from .base import TimestampModel

class LikeModel(TimestampModel, table=True):
    __tablename__ = "likes"
    user_id: uuid_pkg.UUID = Field(primary_key=True, foreign_key="users.id")
    post_id: uuid_pkg.UUID = Field(primary_key=True, foreign_key="posts.id")