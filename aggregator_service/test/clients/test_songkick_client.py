from mock import patch, Mock
from unittest import TestCase
from aggregator_service.clients.songkick import SongkickClient

API_KEY = "apikey"

MOCKED_RESPONSE = {
    "resultsPage": {
        "status": "ok",
        "results": {
            "event": {
                "series": {
                    "displayName": "Glastonbury Festival"
                },
                "type": "Festival",
                "performance": [
                    {
                        "artist": {
                            "displayName": "Radiohead",
                        },
                    },
                    {
                        "artist": {
                            "displayName": "Ed Sheeran",
                        },
                    },
                    {
                        "artist": {
                            "displayName": "Foo Fighters",
                        },
                    }
                ]
            }
        }
    }
}


class TestSongkickClient(TestCase):

    def setUp(self):
        self.songkick_client = SongkickClient(API_KEY)

    def test_init(self):
        self.assertEquals(API_KEY, self.songkick_client._api_key)

    @patch("aggregator_service.clients.songkick.requests.get")
    def test_get_performers(self, requests_get):
        expected = ["Radiohead", "Ed Sheeran", "Foo Fighters"]

        mock_raw_response = Mock()
        mock_raw_response.json.return_value = MOCKED_RESPONSE
        requests_get.return_value = mock_raw_response

        performers = self.songkick_client.get_performers(
            "glastonbury-event-id"
        )

        self.assertEquals(len(expected), len(performers))
        self.assertEquals(sorted(expected), sorted(performers))
        requests_get.assert_called_once_with(
            "https://api.songkick.com"
            "/api/3.0"
            "/events/glastonbury-event-id.json?"
            "apikey=apikey"
        )

    def test_get_performers_when_none_listed(self):
        self.fail()

    def test_get_performers_failure(self):
        self.fail()
