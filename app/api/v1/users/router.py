from fastapi import APIRouter, Depends, Response, status

from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.db import db_session
from app.utils.crypto import hash_password
from .schema import RegisterSchema
from .service import UserService

router = APIRouter()


@router.post("/register")
async def register(user: RegisterSchema, session: AsyncSession = Depends(db_session)):
    user_service = UserService(session)

    hash = hash_password(user.password)
    new_user = await user_service.create_user(
        username=user.username,
        display_name=user.display_name,
        secret=hash
    )
    return new_user


@router.get("/{username}")
async def get_user(username: str, response: Response, session: AsyncSession = Depends(db_session)):
    user_service = UserService(session)

    user = await user_service.get_user_by_username(username)
    result = user.first()
    if result == None:
        response.status_code = status.HTTP_404_NOT_FOUND
    
    return result