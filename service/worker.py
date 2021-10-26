import logging
import random
import time

from service.clients import backend, vkclient
from service.config import access_token, backend_url

logger = logging.getLogger(__name__)


class Worker:

    def __init__(self) -> None:
        self.vk = vkclient.VKClient(access_token, chunk=1)
        self.backend = backend.BackClient(backend_url)

    def work(self) -> None:
        walls = self.backend.get_walls()
        for wall in walls:
            owner_id = wall['wall_id']
            last_post_id = wall['last_post_id']

            time_delay = random.randrange(60, 360)

            while True:
                time.sleep(time_delay)
                new_post = self.vk.get_posts(owner_id, offset=0)[0]
                if new_post.uid > last_post_id:
                    saved_post = self._convert(new_post)
                    self.backend.send_post(saved_post)
                else:
                    logger.info("There are no new messages")
                    continue

    def _convert(self, post: vkclient.Post) -> backend.Post:
        return backend.Post(
            uid=post.uid,
            created=post.created,
            wall=post.wall_id,
            author=post.author_id,
            link=post.link,
            likes=post.likes,
            reposts=post.reposts,
            comments=post.comments,
            views=post.views,
            text=post.text,
        )
