from unittest import TestCase
from datalayer.mongobridge import MongoBridge
from applayer.artist import Artist
from applayer.collaboration import Collaboration


class TestCollaboration(TestCase):

    def setUp(self):
        mb = MongoBridge()
        self.a0 = Artist(mb.get_artist_by_id(1141491))
        self.a1 = Artist(mb.get_artist_by_id(938895))
        self.roles = ["Guitar", "Banjo"]
        self.collab = Collaboration(self.a0, self.a1, self.roles)

        self.a2 = Artist(mb.get_artist_by_id(2411933))
        self.a3 = Artist(mb.get_artist_by_id(2304638))
        self.collab2 = Collaboration(self.a2, self.a3)

    def test_artist0(self):
        self.assertEqual(self.a0, self.collab.artist0)

    def test_not_artist0(self):
        self.assertNotEqual(self.a1, self.collab.artist0)

    def test_artist1(self):
        self.assertEqual(self.a1, self.collab.artist1)

    def test_not_artist1(self):
        self.assertNotEqual(self.a0, self.collab.artist1)

    def test_roles(self):
        self.assertEqual(self.roles, self.collab.roles)
        self.assertIn("Guitar", self.collab.roles)
        self.assertIn("Banjo", self.collab.roles)
        self.assertNotIn("Fiddle", self.collab.roles)

    def test_none_roles(self):
        self.assertIsNone(self.collab2.roles)
