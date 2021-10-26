import logging

import httpx
import orjson

from service.clients.backend.serializers import Post
from service.config import backend_config


logger = logging.getLogger(__name__)


class BackClient:

    def __init__(self, url: str) -> None:
        self.url = url

    def send_post(self, post: Post) -> None:
        try:
            httpx.post(
                url=self.url,
                content=orjson.dumps(post),
                headers={'content-type': 'application/json'},
            )
            logger.debug('new message have been sent to backend')
        except httpx.ConnectError:
            logger.debug('can\'t send message due to connection problem')

    def get_walls(self):
        try:
            response = httpx.get(backend_config)
            walls = response.json()
            logger.debug('walls config has been recieved')
        except httpx.ConnectError:
            logger.debug('can\'t recieve walls config due to connection problem')

        return walls
