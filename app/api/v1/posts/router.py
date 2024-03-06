from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid

from app.db.db import db_session
from app.deps.auth import get_sub

from .service import PostService
from .schema import CreatePostSchema

router = APIRouter()


@router.post("/")
async def create_new_post(request: CreatePostSchema, session: AsyncSession = Depends(db_session), sub: str = Depends(get_sub)):
    post_service = PostService(session)

    new_post = await post_service.create_post(
        author_id=uuid.UUID(sub),
        content=request.content
    )

    return new_post
