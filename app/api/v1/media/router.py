from fastapi import APIRouter, Depends, status, HTTPException, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid

from app.db.db import db_session
from app.deps.auth import get_sub

from .service import MediaService

router = APIRouter()


@router.post("/upload")
async def upload_media(media: UploadFile | None, session: AsyncSession = Depends(db_session), sub: str = Depends(get_sub)):
    if not media:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded",
        )
    
    if "image" not in media.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploader currently only accepts images",
        )
    
    media_service = MediaService(session)

    try:
        new_media = await media_service.upload_media(
            uploader_id=uuid.UUID(sub),
            media=media,
        )
        return new_media
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File is not supported by the server",
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Media does not comply with TOS",
        )