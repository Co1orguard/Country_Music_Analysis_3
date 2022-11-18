from unittest import TestCase
import datalayer.artistnotfound
from datalayer.mongobridge import MongoBridge
from datalayer.artistnotfound import ArtistNotFound
from pymongo.errors import ServerSelectionTimeoutError
import pymongo


class TestMongoBridge(TestCase):

    def setUp(self) -> None:
        self.mongo_bridge = MongoBridge("mongodb://localhost:27017/", "BristolData", "Artists")
        # setUp
        collaborators = [{"collaboratorName": "Barbara Gannod",
                          "collaboratorID": "T?",
                          "releaseID": 1998,
                          "roles": ["Spouse", "Colleague"]}]
        self.test_artist_dictionary = {"artistName": "Jerry Gannod",
                                  "artistID": -237417,
                                  "realname": "Gerald C. Gannod",
                                  "profile": "Supreme leader of the universe",
                                  "collaborators": collaborators,
                                  "level": 42}

    def tearDown(self) -> None:
        pass

    def test_get_all_artists(self):
        artists = self.mongo_bridge.get_all_artists()
        self.assertEqual(179, len(artists))
        a0 = next(item for item in artists if item["artistID"] == 1826136)["artistName"]
        self.assertEqual("Stephen Tarter", a0)
        a1 = next(item for item in artists if item["artistID"] == 628155)["artistName"]
        self.assertEqual("A. P. Carter", a1)

    def test_get_no_artists(self):
        """
        Assumes that you have created an empty collection called "NoArtists"
        """
        with self.assertRaises(ArtistNotFound):
            self.mongo_bridge = MongoBridge("mongodb://localhost:27017/", "BristolData", "NoArtists")
            artists = self.mongo_bridge.get_all_artists()

    def test_get_artists_from_list(self):
        ids = [938895, 2634203, 1141486, 908705, 2411933, 2304638, 3895080, 1448909, 1448911, 1141474, 2916175, 353265, 1141476, 938862, 1141491, 1141484, 1141487, 307357, 1141480, 516930, 1001138, 1141475, 269365, 1141488, 1141483, 1141489, 2867358, 2867360, 2189637, 908699, 1420640, 2867359, 1826135]
        artists = self.mongo_bridge.get_artists_from_list(ids)
        self.assertEqual(33, len(artists))
        # tests whether the artistID at artists[2] is 1141486
        self.assertEqual(1141486, artists[2]["artistID"])
        ids_more = [2411933, 2304638, 3895080]
        moreartists = self.mongo_bridge.get_artists_from_list(ids_more)
        self.assertEqual(3, len(moreartists))

    def test_get_artists_from_bogus_list(self):
        # First part is good; skips the -1 but adds the good items; i.e., do not throw the baby out with the bathwater
        # Bonus points for those that catch this
        ids = [938895, -1, 269365]
        artists = self.mongo_bridge.get_artists_from_list(ids)
        self.assertEqual(2, len(artists))


    def test_get_artist_by_id(self):
        # Artist exists
        artist = self.mongo_bridge.get_artist_by_id(269365)
        self.assertEqual(269365, artist["artistID"])
        self.assertEqual("Jimmie Rodgers", artist["artistName"])
        self.assertEqual(0, artist["level"])
        self.assertEqual("James Charles Rodgers", artist["realname"])
        artist1 = self.mongo_bridge.get_artist_by_id(2411933)
        self.assertEqual("Shortbuckle Roark & Family", artist1["artistName"])

    def test_get_artist_by_id_not_found(self):
        # should fail and thus raise the exception
        ids = [-1]
        with self.assertRaises(ArtistNotFound):
            artists = self.mongo_bridge.get_artists_from_list(ids)

    def test_uri_not_defined(self):
        with self.assertRaises(ServerSelectionTimeoutError):
            self.mongo_bridge = MongoBridge("mongodb://nohost:27017/", "Blah", "Artists")
            artist = self.mongo_bridge.get_artist_by_id(269365)

    def test_add_artist_by_dict(self):

        # Verify that the object is not already in the database
        with self.assertRaises(ArtistNotFound):
            self.mongo_bridge.get_artist_by_id(-237417)
        # Add the artist
        result = self.mongo_bridge.add_artist(self.test_artist_dictionary)
        self.assertTrue(result)
        # Verify the result
        local_artist = self.mongo_bridge.get_artist_by_id(-237417)
        self.assertEqual("Jerry Gannod", local_artist["artistName"])
        self.assertEqual("Gerald C. Gannod", local_artist["realname"])
        self.assertEqual(42, local_artist["level"])
        self.assertEqual("Supreme leader of the universe", local_artist["profile"])
        # Tear this down immediately
        mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mycollection = mongoclient["BristolData"]["Artists"]
        mycollection.delete_one({"artistID": -237417})

    def test_add_artist_by_params(self):

        # Verify that the object is not already in the database
        with self.assertRaises(ArtistNotFound):
            self.mongo_bridge.get_artist_by_id(-237417)
        # Add the artist
        local_in = self.test_artist_dictionary
        result = self.mongo_bridge.add_artist(local_in["artistName"],
                                              local_in["artistID"],
                                              local_in["realname"],
                                              local_in["profile"],
                                              local_in["collaborators"],
                                              local_in["level"])
        self.assertTrue(result)
        # Verify the result
        local_artist = self.mongo_bridge.get_artist_by_id(-237417)
        self.assertEqual("Jerry Gannod", local_artist["artistName"])
        self.assertEqual("Gerald C. Gannod", local_artist["realname"])
        self.assertEqual(42, local_artist["level"])
        self.assertEqual("Supreme leader of the universe", local_artist["profile"])
        # Tear this down immediately
        mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mycollection = mongoclient["BristolData"]["Artists"]
        mycollection.delete_one({"artistID": -237417})
