import uuid
from copy import deepcopy

from fastapi import Depends
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.db import db_session
from app.db.models.post import PostModel
from app.db.models.like import LikeModel
from app.db.models.user import UserModel
from app.db.models.media import MediaModel
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
        statement = self.__get_full_post_request_statement().where(
            PostModel.author_id == author_id,
        ).order_by(
            desc(PostModel.created_at),
            PostModel.id
        )

        result = await self.session.exec(statement)
        result = result.all()

        if result is None or result.__len__() == 0:
            raise FileNotFoundError()
        
        posts = []
        current_id = result[0].PostModel.id
        post_media = []

        for index, post in enumerate(result):
            if post.PostModel.id != current_id:                
                posts.append({
                    "id": result[index-1].PostModel.id,
                    "content": result[index-1].PostModel.content,
                    "media": deepcopy(post_media),
                    "like_count": result[index-1].PostModel.like_count,
                    "author": {
                        "username": result[index-1].UserModel.username,
                        "display_name": result[index-1].UserModel.display_name,
                    },
                    "created_at": result[index-1].PostModel.created_at,
                    "updated_at": result[index-1].PostModel.created_at,
                })
                post_media.clear()
                current_id = post.PostModel.id

            if post.MediaModel is not None:
                post_media.append(f"{post.MediaModel.id}{post.MediaModel.extension}")

        posts.append({
            "id": result[-1].PostModel.id,
            "content": result[-1].PostModel.content,
            "media": deepcopy(post_media),
            "like_count": result[-1].PostModel.like_count,
            "author": {
                "username": result[-1].UserModel.username,
                "display_name": result[-1].UserModel.display_name,
            },
            "created_at": result[-1].PostModel.created_at,
            "updated_at": result[-1].PostModel.created_at,
        })

        return posts
        

    async def get_post(self, post_id: uuid.UUID):
        statement = self.__get_full_post_request_statement().where(
            PostModel.id == post_id,
        )

        result = await self.session.exec(statement)
        result = result.all()

        if result is None or result.__len__() == 0:
            raise FileNotFoundError()

        post_media = []
        for post in result:
            if post.MediaModel is not None:
                post_media.append(f"{post.MediaModel.id}{post.MediaModel.extension}")
        
        post = {
            "id": result[0].PostModel.id,
            "content": result[0].PostModel.content,
            "media": post_media,
            "like_count": result[0].PostModel.like_count,
            "author": {
                "username": result[0].UserModel.username,
                "display_name": result[0].UserModel.display_name,
            },
            "created_at": result[0].PostModel.created_at,
            "updated_at": result[0].PostModel.created_at,
        }

        return post
    

    async def update_post_content(self, post_id: uuid.UUID, user_id: uuid.UUID, content: str):
        statement = select(PostModel).where(PostModel.id == post_id)
        result = await self.session.exec(statement)
        post = result.first()

        if post == None:
            raise FileNotFoundError()
        
        if post.author_id != user_id:
            raise PermissionError()
        
        post.content = content

        self.session.add(post)
        await self.session.commit()

        return await self.get_post(post_id)
    

    async def add_post_media(self, post_id: uuid.UUID, user_id: uuid.UUID, media_id: uuid.UUID):
        statement = select(PostModel).where(PostModel.id == post_id)
        result = await self.session.exec(statement)
        post = result.first()

        if post is None:
            raise FileNotFoundError()
        
        if post.author_id != user_id:
            raise PermissionError()
        
        statement = select(MediaModel).where(MediaModel.id == media_id)
        result = await self.session.exec(statement)
        media = result.first()

        if media is None or media.uploader_id != user_id:
            raise ValueError()
        
        post_media = PostMediaModel(
            post_id=post_id,
            media_id=media_id,
        )

        self.session.add(post_media)
        await self.session.commit()

        return await self.get_post(post_id)
    

    async def delete_post_media(self, post_id: uuid.UUID, user_id: uuid.UUID, media_id: uuid.UUID):
        statement = select(PostModel).where(PostModel.id == post_id)
        result = await self.session.exec(statement)
        post = result.first()

        if post is None:
            raise FileNotFoundError()
        
        if post.author_id != user_id:
            raise PermissionError()
        
        statement = select(MediaModel).where(MediaModel.id == media_id)
        result = await self.session.exec(statement)
        media = result.first()

        if media is None or media.uploader_id != user_id:
            raise ValueError()
        
        statement = select(PostMediaModel).where(
            PostMediaModel.post_id == post_id,
            PostMediaModel.media_id == media_id,
        )
        result = await self.session.exec(statement)
        post_media = result.first()

        await self.session.delete(post_media)
        await self.session.commit()

        return await self.get_post(post_id)


    async def delete_post(self, post_id: uuid.UUID, user_id: uuid.UUID):
        statement = select(PostModel).where(PostModel.id == post_id)
        result = await self.session.exec(statement)
        post = result.first()

        if post == None:
            raise FileNotFoundError()
        
        if post.author_id != user_id:
            raise PermissionError()
        
        await self.session.delete(post)
        await self.session.commit()

        return None
    

    async def like_post(self, post_id: uuid.UUID, user_id: uuid.UUID):
        statement = select(PostModel).where(PostModel.id == post_id)
        result = await self.session.exec(statement)
        post = result.first()

        if post == None:
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
        
        return post.like_count
    

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

        return post.like_count
    

    async def get_post_likes(self, post_id: uuid.UUID):
        statement = select(
            LikeModel,
            UserModel.username,
            UserModel.display_name,
        ).where(LikeModel.post_id == post_id).join(UserModel).order_by(desc(LikeModel.created_at))
        result = await self.session.exec(statement)
        likes = result.all()
        
        users = []
        for like in likes:
            users.append({
                "username": like.username,
                "display_name": like.display_name,
            })

        return {
            "post_id": post_id,
            "like_count": likes.__len__(),
            "users": users,
        }
    

    def __get_full_post_request_statement(self):
        statement = select(
            PostModel,
            UserModel,
            PostMediaModel,
            MediaModel,
        ).join(
            UserModel,
            PostModel.author_id == UserModel.id,
        ).join(
            PostMediaModel,
            PostMediaModel.post_id == PostModel.id,
            isouter=True,
        ).join(
            MediaModel,
            PostMediaModel.media_id == MediaModel.id,
            isouter=True,
        )

        return statement