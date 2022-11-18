from unittest import TestCase
from datalayer.discogsbridge import DiscogsBridge
from datalayer.artistnotfound import ArtistNotFound


class TestDiscogsBridge(TestCase):

    def setUp(self) -> None:
        key = "vjKRGQQBIgvJfZxcTCCK"
        secret = "QNyFiIGvJejsGfjBLxjYQhOIlMiAfFQL"
        self.discogs_bridge = DiscogsBridge(key, secret)
        self.artist = self.discogs_bridge.get_artist_by_id(1141491, 1928)

    def test_get_artist_by_id(self):
        # Artist exists
        self.artist = self.discogs_bridge.get_artist_by_id(1141491, 1928)
        self.assertEqual(1141491, self.artist["artistID"])
        self.assertEqual(0, self.artist["level"])

        # Artist exists
        artist = self.discogs_bridge.get_artist_by_id(1141486, 1928)
        self.assertEqual(1141486, artist["artistID"])
        self.assertEqual(15, len(artist["collaborators"]))
        self.assertEqual(0, artist["level"])

    def test_get_artist_id_collaborators(self):
        self.assertEqual(4, len(self.artist["collaborators"]))
        wd = self.artist["collaborators"][2]
        self.assertEqual(8401049, wd['releaseID'])
        self.assertIn("Written-By", wd['roles'])

    def test_get_noartist_by_id(self):
        with self.assertRaises(ArtistNotFound):
            artist = self.discogs_bridge.get_artist_by_id(-1)
            self.assertEqual(-1, artist["artistID"])

    def test_get_artists_from_list(self):
        """
        This test is SLOW...
        """
        ids = [938895, 1141486]
        artists = self.discogs_bridge.get_artists_from_list(ids)
        self.assertEqual(2, len(artists))
        # tests whether the artistID at artists[2] is 1141486
        self.assertEqual(1141486, artists[1]["artistID"])
        ids_more = [2411933, 2304638]
        moreartists = self.discogs_bridge.get_artists_from_list(ids_more)
        self.assertEqual(2, len(moreartists))

