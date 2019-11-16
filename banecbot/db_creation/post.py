import vk
from datetime import datetime
from functools import lru_cache

from conf import VK_ACCESS_TOKEN


class Post:
    def __init__(self, id_, date, text, likes):
        self.id_ = id_
        self.date = date
        self.text = text
        self.likes = likes

        self.vk_api = vk.API(vk.Session(access_token=VK_ACCESS_TOKEN))

    @property
    def month(self):
        return datetime.utcfromtimestamp(self.date).month

    @property
    def weekday(self):
        return datetime.utcfromtimestamp(self.date).weekday()
