import logging

import httpx
import orjson

from service.clients.backend.serializers import Comment, Post


logger = logging.getLogger(__name__)


class BackClient:

    def __init__(self, url: str) -> None:
        self.url = url

    def send_post(self, post: Post) -> None:
        try:
            httpx.post(
                url=f'{self.url}/api/v1/messages',
                content=orjson.dumps(post),
                headers={'content-type': 'application/json'},
            )
            logger.debug('new message has been sent to backend')
        except httpx.ConnectError:
            logger.debug('can\'t send message due to connection problem')

    def send_comment(self, post: Comment) -> None:
        try:
            httpx.post(
                url=f'{self.url}/api/v1/comments',
                content=orjson.dumps(post),
                headers={'content-type': 'application/json'},
            )
            logger.debug('new comment has been sent to backend')
        except httpx.ConnectError:
            logger.debug('can\'t send comment due to connection problem')

    def get_walls(self):
        try:
            response = httpx.get(f'{self.url}/api/v1/walls/')
            walls = response.json()
            logger.debug('walls config has been recieved')
        except httpx.ConnectError:
            logger.debug('can\'t recieve walls config due to connection problem')

        return walls
