from typing import Any
from glom import glom
import arrow
import httpx

from service.clients.vkclient.serializers import Post


class VKClient:
    url = 'https://api.vk.com/method/wall.get'
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

        response = httpx.get(self.url, params=data)
        response.raise_for_status()

        posts = response.json()['response']['items']
        print(posts)
        return [self._convert(post, owner_id) for post in posts]

    def _convert(self, post: dict[str, Any], owner_id: int) -> Post:
        post_id = glom(post, 'id', default=None)
        return Post(
            uid=int(post_id),
            created=arrow.get(post['date']).datetime,
            author_id=post['from_id'],
            link=f'https://vk.com/wall{owner_id}_{post_id}',
            likes=glom(post, 'likes.count', default=0),
            reposts=glom(post, 'reposts.count', default=0),
            comments=glom(post, 'comments.count', default=0),
            views=glom(post, 'views.count', default=0),
            text=glom(post, 'text', default=None),
        )
