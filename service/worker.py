import logging
import random
import time

from service.clients import backend, vkclient
from service.config import access_token, backend_url, time_delay

logger = logging.getLogger(__name__)


class Worker:

    def __init__(self) -> None:
        self.vk = vkclient.VKClient(access_token, chunk=1)
        self.backend = backend.BackClient(backend_url)
        self.delay = int(time_delay)

    def work(self) -> None:
        while True:
            walls = self.backend.get_walls()
            if not walls:
                logger.debug('Can\'t receive a config from backend. I will try once again in 5 minutes')
                time.sleep(self.delay)
            else:
                for wall in walls:
                    owner_id = wall['wall_id']
                    last_post_id = wall['last_post_id']
                    new_post = self.vk.get_posts(owner_id, offset=0)[0]
                    if new_post.uid <= last_post_id:
                        logger.debug(f"There are no new messages on wall {owner_id}")
                        continue
                    saved_post = self._convert_post(new_post)
                    self.backend.send_post(saved_post)
                    time.sleep(random.randrange(3, 10))
                logger.debug('I am waiting in 5 minutes to make a new query')
                time.sleep(self.delay)

    def _convert_post(self, post: vkclient.Post) -> backend.Post:
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

    def _convert_comment(self, comment: vkclient.Comment) -> backend.Comment:
        return backend.Comment(
            uid=comment.uid,
            post_id=comment.post_id,
            wall_id=comment.wall_id,
            author_id=comment.author_id,
            text=comment.text,
            date_of_publishing=comment.created,
        )
