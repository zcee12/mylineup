from mock import Mock, sentinel
from unittest import TestCase
from aggregator_service.clients.spotify import SpotifyClient
from spotipy.client import SpotifyException


CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"


class TestSpotifyClient(TestCase):

    def setUp(self):
        self.mock_spotipy = Mock()
        self.spotify_client = SpotifyClient(self.mock_spotipy)

    def test_init(self):
        self.assertEquals(
            self.mock_spotipy,
            self.spotify_client._spotipy_client
        )

    def test_get_artist_uri(self):
        mocked_response = {
            'artists': {
                'items': [{
                    'name': 'Craig David',
                    'uri': 'spotify:artist:2JyWXPbkqI5ZJa3gwqVa0c'
                }]
            }
        }
        self.mock_spotipy.search.return_value = mocked_response

        result = self.spotify_client.get_artist_uri(sentinel.CraigDavid)

        self.mock_spotipy.search.assert_called_once_with(
            sentinel.CraigDavid, type="artist", limit=1
        )
        self.assertEqual(
            "spotify:artist:2JyWXPbkqI5ZJa3gwqVa0c",
            result
        )

    def test_get_artist_uri_when_none_found(self):
        mocked_response = {
            'artists': {
                'items': [],
            }
        }
        self.mock_spotipy.search.return_value = mocked_response

        result = self.spotify_client.get_artist_uri(sentinel.NobodyFamous)

        self.mock_spotipy.search.assert_called_once_with(
            sentinel.NobodyFamous, type="artist", limit=1
        )
        self.assertEqual(None, result)

    def test_get_artist_uri_failure(self):
        self.mock_spotipy.search.side_effect = SpotifyException(401, 99, "msg")
        self.assertRaises(
            SpotifyException, self.spotify_client.get_artist_uri, "")

    def test_get_related_artists(self):
        pass

    def test_get_related_artists_failure(self):
        pass
