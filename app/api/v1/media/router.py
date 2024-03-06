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

    new_media = await media_service.upload_media(
        uploader_id=uuid.UUID(sub),
        media=media,
    )

    if new_media is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is not supported by the server",
        )

    return new_media
