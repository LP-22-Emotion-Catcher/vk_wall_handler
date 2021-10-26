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


@dataclass
class Wall:
    wall_id: int
    last_post_id: int


@dataclass
class Comment:
    uid: int
    post_id: int
    wall_id: int
    author_id: int
    text: str
    date_of_publishing: datetime
