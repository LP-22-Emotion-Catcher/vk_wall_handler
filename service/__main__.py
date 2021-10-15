import logging
import random
import time

import arrow
import httpx
import orjson
from glom import glom
from service.clients import vkclient

from service.config import access_token, backend_url, owner_id
from service import domain

logger = logging.getLogger(__name__)


def convert(post: vkclient.Post, owner_id: int) -> domain.Post:
    post_id = glom(post, 'id', default=None)

    return domain.Post(
        uid=int(post_id),
        created=arrow.get(post.created),
        author_id=post.author_id,
        link=f'https://vk.com/wall{owner_id}_{post_id}',
        likes=glom(post, 'likes.count', default=0),
        reposts=glom(post, 'reposts.count', default=0),
        comments=glom(post, 'comments.count', default=0),
        views=glom(post, 'views.count', default=0),
        text=glom(post, 'text', default=None),
    )


def send_post(post: domain.Post):
    try:
        httpx.post(backend_url, json=orjson.dumps(post))
        print('new message have been sent to backend')
    except httpx.ConnectError:
        print('can\'t send message due to connection problem')


if __name__ == "__main__":
    vk = vkclient.VKClient(access_token, chunk=1)

    time_delay = random.randrange(60, 360)

    posts = vk.get_posts(owner_id, offset=0)
    last_post = posts[0]

    saved_post = convert(last_post, owner_id)
    send_post(saved_post)

    while True:
        time.sleep(time_delay)
        new_post = vk.get_posts(owner_id, offset=0)
        new_post_date = new_post[0].created
        if new_post_date > last_post.created:
            saved_post = convert(last_post, owner_id)
            formatted_last_post_date = new_post_date
            send_post(saved_post)
        else:
            print("There are no new messages")
            continue
