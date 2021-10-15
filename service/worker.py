import logging
import random
import time

from glom import glom

from service.clients import backend, vkclient
from service.config import access_token, backend_url, owner_id

logger = logging.getLogger(__name__)


class Worker:

    def __init__(self) -> None:
        self.vk = vkclient.VKClient(access_token, chunk=1)
        self.backend = backend.BackClient(backend_url)

    def work(self) -> None:

        time_delay = random.randrange(60, 360)

        last_post = self.vk.get_posts(owner_id, offset=0)[0]
        saved_post = self._convert(last_post, owner_id)
        self.backend.send_post(saved_post)

        while True:
            time.sleep(time_delay)
            new_post = self.vk.get_posts(owner_id, offset=0)[0]
            if new_post.created > last_post.created:
                last_post = new_post
                saved_post = self._convert(last_post, owner_id)
                self.backend.send_post(saved_post)
            else:
                logger.info("There are no new messages")
                continue

    def _convert(self, post: vkclient.Post, owner_id: int) -> backend.Post:
        post_id = glom(post, 'id', default=None)

        return backend.Post(
            uid=int(post_id),
            created=post.created,
            author=post.author_id,
            link=f'https://vk.com/wall{owner_id}_{post_id}',
            likes=glom(post, 'likes.count', default=0),
            reposts=glom(post, 'reposts.count', default=0),
            comments=glom(post, 'comments.count', default=0),
            views=glom(post, 'views.count', default=0),
            text=glom(post, 'text', default=None),
        )
