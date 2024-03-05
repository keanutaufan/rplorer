from fastapi import APIRouter, Depends, Response, status, HTTPException

from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.db import db_session
from app.utils.crypto import hash_password, verify_hash, check_needs_rehash
from app.utils.token import issue_access_token
from app.deps.auth import get_sub
from .schema import RegisterSchema, LoginSchema
from .service import UserService

router = APIRouter()


@router.post("/register")
async def register(request: RegisterSchema, session: AsyncSession = Depends(db_session)):
    user_service = UserService(session)

    hash = hash_password(request.password)
    new_user = await user_service.create_user(
        username=request.username,
        display_name=request.display_name,
        secret=hash
    )
    return new_user


@router.post("/login")
async def login(request: LoginSchema, response: Response, session: AsyncSession = Depends(db_session)):
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


@router.get("/me")
async def get_me(session: AsyncSession = Depends(db_session), sub: str = Depends(get_sub)):
    user_service = UserService(session)

    user = await user_service.get_user_by_id(sub)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )
    
    return user


@router.get("/{username}")
async def get_user(username: str, session: AsyncSession = Depends(db_session)):
    user_service = UserService(session)

    user = await user_service.get_user_by_username(username)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )
    
    return user