import requests
from requests.exceptions import HTTPError

URL = (
    "https://api.songkick.com"
    "/api/3.0/"
    "events/{event_id}.json?"
    "apikey={api_key}"
)


class SongkickClient(object):

    def __init__(self, api_key):
        self._api_key = api_key

    def get_performers(self, event_id):
        r = requests.get(
            URL.format(event_id=event_id, api_key=self._api_key)
        )
        try:
            r.raise_for_status()
        except HTTPError as e:
            if e.response.status_code == 404:
                raise UnknownSongKickEventError(
                    "{event_id} unknown".format(event_id=event_id)
                )
            raise SongkickClientError(e)

        response = r.json()

        performances = \
            response["resultsPage"]["results"]["event"]["performance"]
        return [
            performance["artist"]["displayName"]
            for performance in performances
        ]


class UnknownSongKickEventError(Exception):
    pass


class SongkickClientError(Exception):
    pass
