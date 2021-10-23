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
        wall = self.backend.get_walls()[0]
        owner_id = wall.wall_id

        time_delay = random.randrange(60, 360)

        last_post = self.vk.get_posts(owner_id, offset=0)[0]
        saved_post = self._convert(last_post)
        self.backend.send_post(saved_post)

        while True:
            time.sleep(time_delay)
            new_post = self.vk.get_posts(owner_id, offset=0)[0]
            if new_post.created > last_post.created:
                last_post = new_post
                saved_post = self._convert(last_post)
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
