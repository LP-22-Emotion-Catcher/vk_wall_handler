import arrow

from dataclasses import dataclass


@dataclass
class Post:
    uid: int
    link: str
    author_id: int
    text: str
    created: arrow.Arrow
    likes: int
    reposts: int
    comments: int
    views: int
