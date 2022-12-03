from typing import List
from multipledispatch import dispatch
import discogs_client
from datalayer.artistnotfound import ArtistNotFound
from discogs_client.exceptions import HTTPError
from discogs_client import Master


class DiscogsBridge(object):
    @dispatch(str, str)
    def __init__(self, key: str, secret: str):
        self.__temp_collaborators: list[dict] = []
        self.__dc: discogs_client.Client = discogs_client.Client(
            'CSC2310_Lecture/1.0',
            consumer_key=key,
            consumer_secret=secret
        )

    @dispatch()
    def __init__(self):
        key = "aIAdnsHNkTEMBYSlURoZ"
        secret = "IDriQOntJdAUodJOKzEPCpKLUSFsclim"
        self.__temp_collaborators: list[dict] = []

        self.__dc: discogs_client.Client = discogs_client.Client(
            'CSC2310_Lecture/1.0',
            consumer_key=key,
            consumer_secret=secret
        )

    def get_artist_by_id(self, aid: int, year: int = 1935) -> dict:
        """
        Get a dictionary of information about an artist from Discogs
        :param aid: artist id
        :param year: optional year
        :return: dictionary with artist info
        :raises: ArtistNotFound if the artist is not found in Discogs
        """
        try:
            temp: discogs_client.Artist = self.__dc.artist(aid)

            retdictionary: dict = {}

            retdictionary["artistID"] = temp.id
            retdictionary["artistName"] = temp.name
            retdictionary["realname"] = temp.real_name
            retdictionary["profile"] = temp.profile
            retdictionary["level"] = 0

            releases = temp.releases
            collaborators: list = []
            duplicates: list = []

            for item in releases:

                if hasattr(item, "year") and 0 < item.year <= year:

                    for track in item.tracklist:
                        extra = track.fetch("extraartists")
                        if extra is not None:
                            tempCollab: dict = {}
                            for extra_artist in extra:
                                tempCollab["collaboratorID"] = extra_artist["id"]
                                tempCollab["collaboratorName"] = extra_artist["name"]
                                tempCollab["releaseID"] = item.id
                                tempCollab["roles"] = extra_artist["role"]

                                if extra_artist["id"] in duplicates:
                                    continue
                                else:
                                    duplicates.append(extra_artist["id"])
                                collaborators.append(tempCollab)
                        else:
                            continue

            currentArtist = {"collaboratorID": temp.id, "collaboratorName": temp.name, "releaseID": None, "role": "root"}

            collaborators.append(currentArtist)
            retdictionary["collaborators"] = collaborators

            return retdictionary
        except HTTPError:
             raise ArtistNotFound("No artists found", 404)

    def get_artists_from_list(self, a_list: list[int], year: int = 1935) -> list[dict]:
        """
        Get all the artists from Discogs based on the input list of int ids
        :param a_list: list of integer ids
        :param year: year filter
        """
        result: List[dict] = []
        for i in a_list:
            a = self.get_artist_by_id(i, year)
            if a is not None:
                result.append(a)
        if not result:
            raise ArtistNotFound("No artists found", 404)
        else:
            return result



