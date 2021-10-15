import logging
import random
import time
from dataclasses import dataclass
from typing import Any

import arrow
import httpx
import orjson
from glom import glom

from service.config import access_token, backend_url, owner_id

logger = logging.getLogger(__name__)


def getjson(url, data=None):
    response = httpx.get(url, params=data)
    return response.json()


@dataclass
class Post:
    uid: int
    link: str
    author_id: int
    text: str
    created: arrow.Arrow
    likes: int
    reposts: int
    comments: int
    views: int


def convert(post: dict[str, Any], owner_id: str) -> Post:
    post_id = glom(post, 'id', default=None)

    return Post(
        uid=int(post_id),
        created=arrow.get(post['date']),
        author_id=post['from_id'],
        link=f'https://vk.com/wall-{owner_id}_{post_id}',
        likes=glom(post, 'likes.count', default=0),
        reposts=glom(post, 'reposts.count', default=0),
        comments=glom(post, 'comments.count', default=0),
        views=glom(post, 'views.count', default=0),
        text=glom(post, 'text', default=None),
    )


def get_new_post(access_token, owner_id, count=1, offset=0):
    """takes access_token, owner_id (group_id), count(default=1), offset(default=0)
    and returns one fresh post from vk group in a dictionary"""
    wall = getjson("https://api.vk.com/method/wall.get", {
            "owner_id": owner_id,
            "count": count,
            "access_token": access_token,
            "offset": offset,
            "v": '5.131'
        })
    post = wall['response']['items']

    return post


def send_post(post: Post):
    try:
        httpx.post(backend_url, json=orjson.dumps(post))
        print('new message have been sent to backend')
    except httpx.ConnectError:
        print('can\'t send message due to connection problem')


if __name__ == "__main__":

    time_delay = random.randrange(60, 360)
    last_post = get_new_post(access_token, owner_id, count=1, offset=0)
    last_post_date = last_post[0]['date']
    formatted_last_post_date = arrow.get(last_post_date)
    current_message = last_post[0]['text']
    saved_post = convert(last_post, owner_id)
    send_post(saved_post)

    while True:
        time.sleep(time_delay)
        new_post = get_new_post(access_token, owner_id, count=1, offset=0)
        new_post_date = new_post[0]['date']
        formatted_new_post_date = arrow.get(new_post_date)
        if formatted_new_post_date > formatted_last_post_date:
            current_message = new_post[0]['text']
            saved_post = convert(last_post, owner_id)
            formatted_last_post_date = formatted_new_post_date
            send_post(saved_post)
        else:
            print("There are no new messages")
            continue
