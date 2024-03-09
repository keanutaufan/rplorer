import uuid

from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.db import db_session
from app.utils.crypto import hash_password, verify_hash, check_needs_rehash
from app.utils.token import issue_access_token
from app.deps.auth import get_sub
from .schema import RegisterSchema, LoginSchema, UserResponseSchema, UserUpdateSchema
from .service import UserService
from ..posts.service import PostService

router = APIRouter()


@router.post("/register")
async def register(request: RegisterSchema, session: AsyncSession = Depends(db_session)) -> UserResponseSchema:
    user_service = UserService(session)

    hash = hash_password(request.password)
    new_user = await user_service.create_user(
        username=request.username,
        display_name=request.display_name,
        secret=hash
    )
    return new_user


@router.post("/login")
async def login(request: LoginSchema, response: Response, session: AsyncSession = Depends(db_session)) -> UserResponseSchema:
    user_service = UserService(session)

    user = await user_service.get_user_by_username(request.username)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )
    
    try:
        verify_hash(user.secret, request.password)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password does not match",
        )
    
    if check_needs_rehash(user.secret):
        user = await user_service.update_password(user.id, request.password)

    token = issue_access_token(user.id)

    response.set_cookie(
        key="Authorization",
        value=token,
        max_age=86400,
        httponly=True,
    )

    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="Authorization",
        httponly=True,
    )

    return {
        "message": "Logout success"
    }


@router.get("/me")
async def get_me(session: AsyncSession = Depends(db_session), sub: str = Depends(get_sub)) -> UserResponseSchema:
    user_service = UserService(session)

    user = await user_service.get_user_by_id(uuid.UUID(sub))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )
    
    return user


@router.patch("/me")
async def update_me(request: UserUpdateSchema, session: AsyncSession = Depends(db_session), sub: str = Depends(get_sub)) -> UserResponseSchema:
    user_service = UserService(session)

    user = await user_service.update_user_by_id(
        id=uuid.UUID(sub),
        display_name=request.display_name,
        bio=request.bio,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )
    
    return user


@router.get("/{username}")
async def get_user(username: str, session: AsyncSession = Depends(db_session)) -> UserResponseSchema:
    user_service = UserService(session)

    user = await user_service.get_user_by_username(username)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )
    
    return user


@router.get("/{username}/posts")
async def get_user_posts(username: str, session: AsyncSession = Depends(db_session)):
    user_service = UserService(session)
    post_service = PostService(session)

    user = await user_service.get_user_by_username(username)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )
    
    try:
        posts = await post_service.get_user_post(user.id)
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
    
    return posts