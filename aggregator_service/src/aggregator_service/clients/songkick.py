import requests

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
        response = r.json()

        performances = \
            response["resultsPage"]["results"]["event"]["performance"]
        return [
            performance["artist"]["displayName"]
            for performance in performances
        ]
