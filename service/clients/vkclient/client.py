import httpx

from service.clients.vkclient.serializers import Post


class VKClient:
    url = 'https://api.vk.com/method/wall.get'
    v_api = '5.131'

    def __init__(self, token: str, chunk: int) -> None:
        self.token = token
        self.chunk = chunk

    def get_posts(self, owner_id: int, offset: int) -> list[Post]:
        data: dict[str, str] = {
            'owner_id': str(owner_id),
            'count': str(self.chunk),
            'access_token': self.token,
            'offset': str(offset),
            'v': self.v_api,
        }

        response = httpx.get(self.url, params=data)
        response.raise_for_status()

        posts = response.json()
        return [Post(**post) for post in posts]
