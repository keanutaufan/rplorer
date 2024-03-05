from fastapi import APIRouter, Depends

from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.db import db_session
from app.utils.crypto import hash_password
from .schema import RegisterSchema
from .service import UserService

router = APIRouter()


@router.get("/register")
async def register(user: RegisterSchema, session: AsyncSession = Depends(db_session)):
    user_service = UserService(session=session)
    
    hash = hash_password(user.password)
    new_user = await user_service.create_user(
        username=user.username,
        display_name=user.display_name,
        secret=hash
    )
    return new_user
