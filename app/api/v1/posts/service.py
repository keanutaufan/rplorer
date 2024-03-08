import uuid

from fastapi import Depends
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.db import db_session
from app.db.models.post import PostModel
from app.db.models.like import LikeModel
from app.db.models.user import UserModel
from app.db.models.post_media import PostMediaModel

class PostService:
    def __init__(self, session: AsyncSession = Depends(db_session)):
        self.session = session
    
    async def create_post(self, author_id: uuid.UUID, content: str, media_id: list[uuid.UUID]):
        post_id = uuid.uuid4()

        new_post = PostModel(
            id=post_id,
            author_id=author_id,
            content=content,
            like_count=0,
        )

        self.session.add(new_post)

        for id in media_id:
            link = PostMediaModel(
                post_id=post_id,
                media_id=id,
            )
            self.session.add(link)

        await self.session.commit()
        await self.session.refresh(new_post)

        return new_post
    
    
    async def get_user_post(self, author_id: uuid.UUID):
        statement = select(PostModel).where(PostModel.author_id == author_id)
        result = await self.session.exec(statement)
        return result.all()
    

    async def get_post(self, post_id: uuid.UUID):
        statement = select(PostModel).where(PostModel.id == post_id)
        result = await self.session.exec(statement)
        return result.first()
    

    async def like_post(self, post_id: uuid.UUID, user_id: uuid.UUID):
        statement = select(PostModel).where(PostModel.id == post_id)
        result = await self.session.exec(statement)
        post = result.first()

        print("post id", post_id)
        print("post", post)
        if post == None:
            print("This is expected")
            return None

        post.like_count = post.like_count + 1
        
        new_like = LikeModel(
            post_id=post_id,
            user_id=user_id,
        )

        self.session.add(new_like)
        self.session.add(post)

        await self.session.commit()
        await self.session.refresh(post)
        
        return post
    

    async def unlike_post(self, post_id: uuid.UUID, user_id: uuid.UUID):
        statement = select(PostModel).where(PostModel.id == post_id)
        result = await self.session.exec(statement)
        post = result.first()

        if post == None:
            return None

        post.like_count = post.like_count - 1
        
        statement = select(LikeModel).where(LikeModel.post_id == post_id, LikeModel.user_id == user_id)
        result = await self.session.exec(statement)
        like = result.first()

        self.session.add(post)
        await self.session.delete(like)

        await self.session.commit()
        await self.session.refresh(post)

        return post
    

    async def get_post_likes(self, post_id: uuid.UUID):
        statement = select(
            LikeModel,
            UserModel.username,
            UserModel.bio,
        ).where(LikeModel.post_id == post_id).join(UserModel).order_by(desc(LikeModel.created_at))
        result = await self.session.exec(statement)
        likes = result.all()
        
        users = []
        for like in likes:
            users.append({
                "username": like.username,
                "bio": like.bio,
            })

        return users