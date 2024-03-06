from fastapi import APIRouter, Depends, status, HTTPException
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


@router.get("/{post_id}")
async def get_post(post_id: str, session: AsyncSession = Depends(db_session)):
    post_service = PostService(session)

    parsed_post_id = None

    try:
        parsed_post_id = uuid.UUID(post_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist"
        )

    post = await post_service.get_post(parsed_post_id)
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist",
        )
    
    return post


@router.post("/{post_id}/likes")
async def like_post(post_id: str, session: AsyncSession = Depends(db_session), sub: str = Depends(get_sub)):
    post_service = PostService(session)

    parsed_post_id = None

    try:
        parsed_post_id = uuid.UUID(post_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist"
        )
    
    
    try:
        post = await post_service.like_post(parsed_post_id, uuid.UUID(sub))
        if post == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post does not exist",
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already liked this post",
        )
    
    return post


@router.delete("/{post_id}/likes")
async def unlike_post(post_id: str, session: AsyncSession = Depends(db_session), sub: str = Depends(get_sub)):
    post_service = PostService(session)

    parsed_post_id = None

    try:
        parsed_post_id = uuid.UUID(post_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist"
        )
    
    
    try:
        post = await post_service.unlike_post(parsed_post_id, uuid.UUID(sub))
        if post == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post does not exist",
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already unliked this post",
        )
    
    return post


@router.get("/{post_id}/likes")
async def get_post_likes(post_id: str, session: AsyncSession = Depends(db_session)):
    post_service = PostService(session)

    parsed_post_id = None

    try:
        parsed_post_id = uuid.UUID(post_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist"
        )
    
    
    likes = await post_service.get_post_likes(parsed_post_id)
    if likes == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist",
        )
    
    return likes