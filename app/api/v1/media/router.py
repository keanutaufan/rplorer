import uuid

from fastapi import APIRouter, Depends, status, HTTPException, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession

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
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error happened",
        )
    

@router.delete("/upload/{media_id}")
async def delete_media(media_id: str, session: AsyncSession = Depends(db_session), sub: str = Depends(get_sub)):
    media_service = MediaService(session)

    parsed_media_id = None

    try:
        parsed_media_id = uuid.UUID(media_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media does not exist"
        )
    
    try:
        await media_service.delete_media(parsed_media_id, uuid.UUID(sub))
        return { "message": "OK" }
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media does not exist",
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only uploader can delete media",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error happened",
        )