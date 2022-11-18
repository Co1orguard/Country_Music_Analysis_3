from applayer.artist import Artist
from typing import List


class Collaboration(object):
    def __init__(self, art0: Artist, art1: Artist, role: List[str] = None):
        self.__artist0: Artist = art0
        self.__artist1: Artist = art1
        self.__roles: List[str] = role

    @property
    def artist0(self):
        return self.__artist0

    @property
    def artist1(self):
        return self.__artist1

    @property
    def roles(self):
        return self.__roles
