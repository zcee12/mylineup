class SpotifyClient(object):

    def __init__(self, spotipy_client):
        self._spotipy_client = spotipy_client

    def get_artist_uri(self, artist):
        response = self._spotipy_client.search(artist, type="artist", limit=1)
        try:
            return response["artists"]["items"][0]["uri"]
        except IndexError:
            return None

    def get_related_artists(self, artist_uri):
        related = self._spotipy_client.artist_related_artists(artist_uri)
        return [artist["name"] for artist in related["artists"]]
