import uuid

from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.db import db_session
from app.db.models.post import PostModel

class PostService:
    def __init__(self, session: AsyncSession = Depends(db_session)):
        self.session = session
    
    async def create_post(self, author_id: uuid.UUID, content: str):
        new_post = PostModel(
            author_id=author_id,
            content=content
        )

        self.session.add(new_post)
        await self.session.commit()
        await self.session.refresh(new_post)

        return new_post
    
    
    async def get_user_post(self, author_id: uuid.UUID):
        statement = select(PostModel).where(PostModel.author_id == author_id)
        result = await self.session.exec(statement)
        return result.all()