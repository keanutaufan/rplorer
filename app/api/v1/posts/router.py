from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid

from app.db.db import db_session
from app.deps.auth import get_sub

from .service import PostService
from .schema import CreatePostSchema, UpdatePostSchema, UpdatePostMediaSchema

router = APIRouter()


@router.post("/")
async def create_new_post(request: CreatePostSchema, session: AsyncSession = Depends(db_session), sub: str = Depends(get_sub)):
    parsed_media_id = []

    try:
        for media_id in request.media:
            parsed_media_id.append(uuid.UUID(media_id))
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media does not exist"
        )
    
    post_service = PostService(session)

    new_post = await post_service.create_post(
        author_id=uuid.UUID(sub),
        content=request.content,
        media_id=parsed_media_id,
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

    try:
        post = await post_service.get_post(parsed_post_id)
        return post
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error happened",
        )



@router.patch("/{post_id}")
async def update_post(post_id: str, request: UpdatePostSchema, session: AsyncSession = Depends(db_session), sub: str = Depends(get_sub)):
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
        post = await post_service.update_post_content(parsed_post_id, uuid.UUID(sub), request.content)
        return post
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist"
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post does not belong to user"
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error happened"
        )


@router.post("/{post_id}/media")
async def add_post_media(post_id: str, request: UpdatePostMediaSchema, session: AsyncSession = Depends(db_session), sub: str = Depends(get_sub)):
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
        parsed_media_id = uuid.UUID(request.media_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media does not exist"
        )

    try:
        post = await post_service.add_post_media(parsed_post_id, uuid.UUID(sub), parsed_media_id)
        return post
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist"
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post does not belong to user"
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Media does not exist"
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already added this media"
        )
    

@router.delete("/{post_id}")
async def update_post(post_id: str, session: AsyncSession = Depends(db_session), sub: str = Depends(get_sub)):
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
        post = await post_service.delete_post(parsed_post_id, uuid.UUID(sub))
        return { "message": "Post deleted" }
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist"
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Post does not belong to user"
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error happened"
        )
        

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
        like_count = await post_service.like_post(parsed_post_id, uuid.UUID(sub))
        if like_count == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post does not exist",
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already liked this post",
        )
    
    return {"like_count": like_count}


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
        like_count = await post_service.unlike_post(parsed_post_id, uuid.UUID(sub))
        if like_count == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post does not exist",
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already unliked this post",
        )
    
    return {"like_count": like_count}


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