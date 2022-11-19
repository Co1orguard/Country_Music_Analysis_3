from unittest import TestCase
from applayer.artistgraph import ArtistGraph
from applayer.artist import Artist
from applayer.collaboration import Collaboration
from applayer.artistlist import ArtistList
from datalayer.mongobridge import MongoBridge


class TestArtistGraph(TestCase):

    def setUp(self) -> None:
        self.artistlist = ArtistList([1141491, 1420640, 2867359])
        self.artistgraph = ArtistGraph(self.artistlist, 3)
        self.a = Artist(0, "Jerry Gannod", "Jerry Gannod", "", 0)
        self.b = Artist(1, "Gerald Gannod", "Gerald Gannod", "", 0)
        self.emptygraph = ArtistGraph()

        # Create a graph using Alfred Karnes
        self.ak_list = ArtistList([1141491])
        self.ak_graph = ArtistGraph(self.ak_list, 2)
        mb = MongoBridge()
        # Get the objects related to William Doane and Alfred Karnes
        self.wd_data = mb.get_artist_by_id(726550)
        self.ak_data = mb.get_artist_by_id(1141491)
        self.wd_artist = Artist(self.wd_data)
        self.ak_artist = Artist(self.ak_data)
        self.gmbb_artist = Artist(4014047, "Grand Massed Brass Bands", "", "", 2)
        # Create a collaboration and ...

    def test_add_collaboration(self):
        c = Collaboration(self.a, self.b)
        self.emptygraph.add_collaboration(c)
        self.assertTrue(self.emptygraph.has_edge(self.a, self.b))
        self.assertTrue(self.emptygraph.has_edge(self.b, self.a))
        self.assertTrue(self.emptygraph.has_node(self.a))
        self.assertTrue(self.emptygraph.has_node(self.b))

    def test_buildgraph(self):
        self.assertEqual(66, len(self.artistgraph.artists))
        self.assertEqual(91, len(self.artistgraph.collaborations))
        self.assertEqual(0, len(self.emptygraph.artists))
        self.assertEqual(0, len(self.emptygraph.collaborations))

    def test_add_artist(self):
        self.emptygraph.add_artist(self.a)
        self.assertTrue(self.emptygraph.has_node(self.a))
        self.assertFalse(self.emptygraph.has_node(self.b))
        self.assertEqual(1, len(self.emptygraph.artists))
        self.assertTrue(1, len(self.emptygraph.graph.nodes))
        self.assertEqual(66, len(self.artistgraph.graph.nodes))

    def test_ak_list(self):
        # Test to see the right number of nodes are there, that William Doane is in the list, and that the edge
        # between these artists are there
        self.assertTrue(33, len(self.ak_graph.graph.nodes))
        self.assertTrue(self.ak_graph.has_node(self.wd_artist))
        self.assertTrue(self.ak_graph.has_edge(self.wd_artist, self.ak_artist))
        self.assertTrue(self.ak_graph.has_edge(self.ak_artist, self.wd_artist))
        self.assertTrue(self.ak_graph.has_node(self.gmbb_artist))
        self.assertTrue(self.ak_graph.has_edge(self.wd_artist, self.gmbb_artist))
        self.assertTrue(self.ak_graph.has_edge(self.gmbb_artist, self.wd_artist))

    def test_compute_degree_centrality(self):
        self.assertTrue(True)

    def test_compute_closeness_centrality(self):
        self.assertTrue(True)

    def test_expansion(self):
        self.assertEqual(33, len(self.artistgraph.get_expansion_list()))