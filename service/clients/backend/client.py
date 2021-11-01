import logging

import httpx
import orjson

from service.clients.backend.serializers import Comment, Post, Wall


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
        except (httpx.ConnectError, httpx.RemoteProtocolError):
            logger.debug('Can\'t send message due to connection problem')

    def send_comment(self, post: Comment) -> None:
        try:
            httpx.post(
                url=f'{self.url}/api/v1/comments',
                content=orjson.dumps(post),
                headers={'content-type': 'application/json'},
            )
            logger.debug('New comment has been sent to backend')
        except (httpx.ConnectError, httpx.RemoteProtocolError):
            logger.debug('Can\'t send comment due to connection problem')

    def get_walls(self):
        try:
            response = httpx.get(f'{self.url}/api/v1/walls/')
            walls = response.json()
            logger.debug('Walls config has been recieved')
        except (httpx.ConnectError, httpx.RemoteProtocolError):
            logger.debug('Can\'t recieve walls config due to connection problem')
            return None
        return walls

    def delete_wall(self, wall: Wall) -> None:
        try:
            httpx.delete(url=f'{self.url}/api/v1/wall/{wall.wall_id}')
            logger.debug('Wall has been sent for deletion')
        except (httpx.ConnectError, httpx.RemoteProtocolError, KeyError):
            logger.debug('Can\'t send wall due to connection problem')
            raise KeyError
