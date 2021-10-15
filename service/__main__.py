import arrow  # для работы с датами
import httpx  # для запроса
import random  # для рандомизации временного интервала
import time  # для задержки между запросами

from service.config import access_token, owner_id, backend_url  # настройки для запроса
from datetime import datetime as dt  # для перевода даты из timestamp
from glom import glom  # для безопасного получения значений словаря


def getjson(url, data=None):
    response = httpx.get(url, params=data)
    return response.json()


def save_post(all_posts):
    """Takes in a list of dictionaries with posts, converts the data
    in a new structure, returns a new list of dictionaries with the posts"""
    filtered_data = []
    for post in all_posts:
        try:
            link = 'https://vk.com/wall-{owner_id}_{id}'.format(
                owner_id=owner_id[1:],
                id=id
                )
        except:
            link = ''
        try:
            date = dt.fromtimestamp(int(post['date'])).strftime('%d-%m-%Y %H:%M:%S')
        except:
            date = ''
        
        post_id = glom(post, 'id', default=None)
        author_id = glom(post, 'from_id', default=None)
        timestamp = glom(post, 'date', default=None)
        likes = glom(post, 'likes.count', default=None)
        reposts = glom(post, 'reposts.count', default=None)
        comments = glom(post, 'comments.count', default=None)
        views = glom(post, 'views.count', default=None)
        text = glom(post, 'text', default=None)
        all_attachments = []
        try:
            attachments = post['attachments']
            if attachments:
                for att in attachments:
                    if att['type'] == 'video':
                        video_title = att['video']['title']
                        all_attachments.append(video_title)
                    if att['type'] == 'photo':
                        photo = att['photo']['text']
                        all_attachments.append(photo)
        except:
            attachments = ''

        filtered_post = {
            'post_id': post_id,
            'author_id': author_id,
            'date': date,
            'timestamp': timestamp,
            'likes': likes,
            'reposts': reposts,
            'comments': comments,
            'views': views,
            'text': text,
            'attachments': all_attachments,
            'link': link,
        }
        filtered_data.append(filtered_post)
    return filtered_data


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


def send_post(post):
    payload = post[0]
    try:
        httpx.post(backend_url, json=payload)
        print('new message have been sent to backend')
    except httpx.ConnectError:
        print('can\'t send message due to connection problem')


if __name__ == "__main__":

    time_delay = random.randrange(60, 360)
    last_post = get_new_post(access_token, owner_id, count=1, offset=0)
    last_post_date = last_post[0]['date']
    formatted_last_post_date = arrow.get(last_post_date)
    current_message = last_post[0]['text']
    saved_post = save_post(last_post)
    send_post(saved_post)

    while True:
        time.sleep(time_delay)
        new_post = get_new_post(access_token, owner_id, count=1, offset=0)
        new_post_date = new_post[0]['date']
        formatted_new_post_date = arrow.get(new_post_date)
        if formatted_new_post_date > formatted_last_post_date:
            current_message = new_post[0]['text']
            saved_post = save_post(last_post)
            formatted_last_post_date = formatted_new_post_date
            send_post(saved_post)
        else:
            print("There are no new messages")
            continue
