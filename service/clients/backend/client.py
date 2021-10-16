import logging


import httpx
import orjson

from service.clients.backend.serializers import Post

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
