from typing import Any
from glom import glom
import arrow
import httpx

from service.clients.vkclient.serializers import Post, Comment


class VKClient:
    posts_url = 'https://api.vk.com/method/wall.get'
    comments_url = 'https://api.vk.com/method/wall.getComments'
    v_api = '5.131'

    def __init__(self, token: str, chunk: int) -> None:
        self.token = token
        self.chunk = chunk

    def get_posts(self, owner_id: int, offset: int) -> list[Post]:
        data: dict[str, str] = {
            'owner_id': str(owner_id),
            'count': str(self.chunk),
            'access_token': self.token,
            'offset': str(offset),
            'v': self.v_api,
        }

        response = httpx.get(self.posts_url, params=data)
        response.raise_for_status()

        posts = response.json()['response']['items']
        return [self._convert_posts(post, owner_id) for post in posts]

    def _convert_posts(self, post: dict[str, Any], owner_id: int) -> Post:
        post_id = glom(post, 'id', default=None)
        return Post(
            uid=int(post_id),
            created=arrow.get(post['date']).datetime,
            wall_id=post['owner_id'],
            author_id=post['from_id'],
            link=f'https://vk.com/wall{owner_id}_{post_id}',
            likes=glom(post, 'likes.count', default=0),
            reposts=glom(post, 'reposts.count', default=0),
            comments=glom(post, 'comments.count', default=0),
            views=glom(post, 'views.count', default=0),
            text=glom(post, 'text', default=None),
        )

    def get_comments(self, owner_id: int, post_id: int, offset: int) -> list[Comment]:
        data: dict[str, str] = {
            'owner_id': str(owner_id),
            'post_id': str(post_id),
            'count': str(self.chunk),
            'sort': 'desc',
            'access_token': self.token,
            'offset': str(offset),
            'v': self.v_api,
        }

        response = httpx.get(self.comments_url, params=data)
        response.raise_for_status()

        comments = response.json()['response']['items']
        return [self._convert_comments(comment, owner_id) for comment in comments]

    def _convert_comments(self, comment: dict[str, Any], owner_id: int) -> Comment:
        comment_id = glom(comment, 'id', default=None)
        return Comment(
            uid=int(comment_id),
            created=arrow.get(comment['date']).datetime,
            wall_id=comment['owner_id'],
            author_id=comment['from_id'],
            post_id=comment['post_id'],
            text=comment['text'],
        )
