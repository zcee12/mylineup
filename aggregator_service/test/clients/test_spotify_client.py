from unittest import TestCase
from aggregator_service.clients.spotify import SpotifyClient


CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"


class TestSpotifyClient(TestCase):

    def setUp(self):
        self.spotify_client = SpotifyClient(
            CLIENT_ID,
            CLIENT_SECRET
        )

    def test_init(self):
        self.assertEquals(
            CLIENT_ID,
            self.spotify_client.client_id
        )
        self.assertEquals(
            CLIENT_SECRET,
            self.spotify_client.client_secret
        )

    def test_get_artist_uri(self):
        pass

    def test_get_artist_uri_failure(self):
        pass

    def test_get_related_artists(self):
        pass

    def test_get_related_artists_failure(self):
        pass
