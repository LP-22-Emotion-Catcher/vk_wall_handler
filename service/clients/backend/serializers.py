from datetime import datetime

from dataclasses import dataclass


@dataclass
class Post:
    uid: int
    link: str
    wall: int
    author: int
    text: str
    created: datetime
    likes: int
    reposts: int
    comments: int
    views: int
