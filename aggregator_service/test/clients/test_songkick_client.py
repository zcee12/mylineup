from mock import patch, Mock
from unittest import TestCase
from aggregator_service.clients.songkick import (
    SongkickClient, SongkickClientError, UnknownSongKickEventError)
from requests.exceptions import HTTPError

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

MOCKED_RESPONSE_NO_PERFORMERS_LISTED = {
    "resultsPage": {
        "status": "ok",
        "results": {
            "event": {
                "series": {
                    "displayName": "Glastonbury Festival"
                },
                "type": "Festival",
                "performance": [
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

    @patch("aggregator_service.clients.songkick.requests.get")
    def test_get_performers_when_none_listed(self, requests_get):
        mock_raw_response = Mock()
        mock_raw_response.json.return_value = \
            MOCKED_RESPONSE_NO_PERFORMERS_LISTED
        requests_get.return_value = mock_raw_response

        performers = self.songkick_client.get_performers(
            "glastonbury-event-id"
        )

        self.assertEquals(0, len(performers))
        requests_get.assert_called_once_with(
            "https://api.songkick.com"
            "/api/3.0"
            "/events/glastonbury-event-id.json?"
            "apikey=apikey"
        )

    @patch("aggregator_service.clients.songkick.requests.get")
    def test_get_performers_unknown_event(self, requests_get):
        mock_raw_response = Mock()
        mock_raw_response.status_code = 404

        exception = HTTPError()
        exception.response = mock_raw_response

        mock_raw_response.raise_for_status.side_effect = exception
        requests_get.return_value = mock_raw_response

        self.assertRaises(
            UnknownSongKickEventError,
            self.songkick_client.get_performers,
            ""
        )

    @patch("aggregator_service.clients.songkick.requests.get")
    def test_get_performers_failure(self, requests_get):
        mock_raw_response = Mock()
        mock_raw_response.status_code = 500

        exception = HTTPError()
        exception.response = mock_raw_response

        mock_raw_response.raise_for_status.side_effect = exception
        requests_get.return_value = mock_raw_response

        self.assertRaises(
            SongkickClientError,
            self.songkick_client.get_performers,
            ""
        )
