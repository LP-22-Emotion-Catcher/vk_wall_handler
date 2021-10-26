from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    uid: int
    link: str
    wall_id: int
    author_id: int
    text: str
    created: datetime
    likes: int
    reposts: int
    comments: int
    views: int


class Comment(BaseModel):
    uid: int
    post_id: int
    wall_id: int
    author_id: int
    text: str
    created: datetime
