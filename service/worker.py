import logging
import random
import time

from service.clients import backend, vkclient
from service.config import access_token, backend_url, backend_comments_url

logger = logging.getLogger(__name__)


class Worker:

    def __init__(self) -> None:
        self.vk = vkclient.VKClient(access_token, chunk=1)
        self.backend_messages = backend.BackClient(backend_url)
        self.backend_comments = backend.BackClient(backend_comments_url)

    def work(self) -> None:
        wall = self.backend_messages.get_walls()[0]
        owner_id = wall['wall_id']
        last_post_id = wall['last_post_id']

        time_delay = random.randrange(60, 360)

        while True:
            time.sleep(time_delay)
            new_post = self.vk.get_posts(owner_id, offset=0)[0]
            if new_post.uid > last_post_id:
                saved_post = self._convert_post(new_post)
                self.backend_messages.send_post(saved_post)
            else:
                logger.info("There are no new messages")
                continue
            comment = self.vk.get_comments(owner_id, post_id=new_post.uid, offset=0)[0]
            saved_comment = self._convert_comment(comment)
            self.backend_comments.send_comment(saved_comment)

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
