import uuid

from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.db import db_session
from app.db.models.user import UserModel
from app.utils.crypto import hash_password

class UserService:
    def __init__(self, session: AsyncSession = Depends(db_session)):
        self.session = session

    async def create_user(self, username: str, secret: str, display_name: str):
        new_user = UserModel(
            username=username,
            secret=secret,
            display_name=display_name,
        )

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def get_user_by_id(self, id: uuid.UUID):
        statement = select(UserModel).where(UserModel.id == id)
        result = await self.session.exec(statement)
        return result.first()
    
    async def get_user_by_username(self, username: str):
        statement = select(UserModel).where(UserModel.username == username)
        result = await self.session.exec(statement)
        return result.first()
    
    async def update_password(self, id: uuid.UUID, new_password: str):
        statement = select(UserModel).where(UserModel.id == id)
        result = await self.session.exec(statement)
        user = result.one()

        new_hash = hash_password(new_password)
        user.secret = new_hash
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user