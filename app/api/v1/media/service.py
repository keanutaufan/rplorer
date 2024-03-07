import uuid
import pathlib
import shutil

from fastapi import Depends, UploadFile
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from decouple import config

from app.db.db import db_session
from app.utils.filter import classify_image
from app.db.models.media import MediaModel
from app.db.models.user import UserModel

from transformers import pipeline

MEDIA_PATH = config("MEDIA_PATH")
IMAGE_FILTER_MODEL_PATH = config("IMAGE_FILTER_MODEL_PATH")
FILTERED_MEDIA_PATH = config("FILTERED_MEDIA_PATH")

pipeline = pipeline("image-classification", model=pathlib.Path("media/nsfw_image_detection"))

class MediaService:
    def __init__(self, session: AsyncSession = Depends(db_session)):
        self.session = session
    
    async def upload_media(self, media: UploadFile, uploader_id: uuid.UUID):
        random_uuid = uuid.uuid4()
        extension = "".join(pathlib.Path(media.filename).suffixes)

        path = pathlib.Path(f"{MEDIA_PATH}/{str(random_uuid)}{extension}")
        try:
            with path.open("wb") as buffer:
                shutil.copyfileobj(media.file, buffer)
        except:
            raise TypeError()
        finally:
            media.file.close()
            
        prediction = classify_image(path, pipeline)
        if prediction != "normal":
            shutil.move(path, pathlib.Path(FILTERED_MEDIA_PATH))
            raise ValueError()

        new_media = MediaModel(
            id=random_uuid,
            uploader_id=uploader_id,
            extension=extension,
        )

        self.session.add(new_media)
        await self.session.commit()
        await self.session.refresh(new_media)

        return new_media