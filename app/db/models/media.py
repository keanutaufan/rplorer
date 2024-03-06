from sqlmodel import Field
import uuid as uuid_pkg

from .base import UUIDModel, TimestampModel

class MediaModel(UUIDModel, TimestampModel, table=True):
    __tablename__ = "media"
    extension: str