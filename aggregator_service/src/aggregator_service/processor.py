import json
from sets import Set


class Processor(object):

    def __init__(self, processed_dir, spotify_client, songkick_client):
        self.processed_dir = processed_dir
        self.spotify_client = spotify_client
        self.songkick_client = songkick_client

    def _get_performer_recommendation(self, job):
        performers = self.songkick_client.get_performers(
            job.event_id
        )

        artist_uris = [
            self.spotify_client.get_artist_uri(artist)
            for artist in job.artists
        ]

        related_artists = []
        for artist_uri in artist_uris:
            related_artists = (
                related_artists
                + self.spotify_client.get_related_artists(artist_uri)
            )

        return Set(performers).intersection(Set(related_artists + job.artists))

    def dispatch(self, job):
        location = "{0}/{1}".format(self.processed_dir, job.id)
        print location
        job.status = "failed"
        with open(location, "wb") as f:
            f.write(json.dumps(job.__dict__))
