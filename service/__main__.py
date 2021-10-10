
import httpx # для запроса

import random # для рандомизации временного интервала
import time # для задержки между запросами

from service.config import access_token, owner_id # настройки для запроса
from datetime import datetime as dt # для перевода даты из timestamp
from glom import glom # для безопасного получения значений словаря

import arrow # для работы с датами


def getjson(url, data=None):
    response = httpx.get(url, params=data)
    return response.json()

def get_all_posts(access_token, owner_id, count=100, offset=0):
    """takes access_token, owner_id (group_id), count(default=100), offset(default=0)
    and returns all posts from vk group in a list of dictionaries
    and the number of posts in second variable"""
    
    all_posts = []
    while True:
        time.sleep(random.random())
        wall = getjson("https://api.vk.com/method/wall.get", {
            "owner_id" : owner_id,
            "count": count,
            "access_token": access_token,
            "offset": offset,
            "v": '5.131'
        })
        count_posts = wall['response']['count']
        posts = wall['response']['items']

        all_posts.extend(posts)

        if len(all_posts) >= count_posts:
            break
        else:
            offset += 100
    
    return all_posts, count_posts


def get_all_posts2(access_token, owner_id, count=5, offset=0):
    """takes access_token, owner_id (group_id), count(default=100), offset(default=0)
    and returns all posts from vk group in a list of dictionaries
    and the number of posts in second variable"""
    
    all_posts = []
    
        
    wall = getjson("https://api.vk.com/method/wall.get", {
            "owner_id" : owner_id,
            "count": count,
            "access_token": access_token,
            "offset": offset,
            "v": '5.131'
        })
    count_posts = wall['response']['count']
    posts = wall['response']['items']

    all_posts.extend(posts)


    
    return all_posts, count_posts



















def make_posts(all_posts):
    """Takes in a list of dictionaries with posts, converts the data
    in a new structure, returns a new list of dictionaries with the posts"""
    filtered_data = []
    for post in all_posts:
        try:
            link = 'https://vk.com/wall-{owner_id}_{id}'.format(owner_id=owner_id[1:], id=id)
        except:
            link = ''
        try:
            date = dt.fromtimestamp(int(post['date'])).strftime('%d-%m-%Y %H:%M:%S')
        except:
            date = ''
        
        id_ = glom(post,'id',default=None)
        timestamp = glom(post,'date',default=None)
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
            'id': id_,
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

if __name__ == "__main__":

    all_posts, count_posts = get_all_posts2(access_token, owner_id, count=2, offset=0)
    print(all_posts)
    print('----------------------------------------------------------------------')
    date = all_posts[0]['date']
    date2 = all_posts[1]['date']
    formatted_date = arrow.get(date)
    formatted_date2 = arrow.get(date2)
   
    if formatted_date > formatted_date2:
        print(f"date {formatted_date} is greater that {formatted_date2}")
    elif formatted_date < formatted_date2:
        print(f"date {formatted_date} is lower than {formatted_date2}")
    else:
        print(f"dates {formatted_date} and {formatted_date2} are equal") 
      