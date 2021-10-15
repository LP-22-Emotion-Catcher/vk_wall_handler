from datetime import datetime

from pydantic import BaseModel


class Post(BaseModel):
    uid: int
    link: str
    author_id: int
    text: str
    created: datetime
    likes: int
    reposts: int
    comments: int
    views: int