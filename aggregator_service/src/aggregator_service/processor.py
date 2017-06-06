import json
import logging
import os
from sets import Set

LOGGER = logging.getLogger(__name__)


class Processor(object):

    def __init__(
            self, pending_dir, processed_dir, spotify_client, songkick_client):
        self.pending_dir = pending_dir
        self.processed_dir = processed_dir
        self.spotify_client = spotify_client
        self.songkick_client = songkick_client

    def _get_performer_recommendation(self, job):
        performers = self.songkick_client.get_performers(
            job.event_id
        )
        logging.debug("{0} performers are {1}".format(job.id, performers))

        artist_uris = [
            self.spotify_client.get_artist_uri(artist)
            for artist in job.artists
        ]

        related_artists = []
        for artist_uri in artist_uris:
            logging.debug("{0} Working on {1}".format(job.id, artist_uri))
            logging.debug(
                "{0} related artists {1}".format(job.id, related_artists))

            r = self.spotify_client.get_related_artists(artist_uri)
            related_artists = related_artists + r

        return list(
            Set(performers).intersection(Set(related_artists + job.artists)))

    def dispatch(self, job):
        pending_location = os.path.join(self.pending_dir, job.id)
        processed_location = os.path.join(self.processed_dir, job.id)

        logging.info("Started job " + job.id)
        logging.debug(
            "{0} done location is {1}".format(job.id, processed_location))

        try:
            job.result = self._get_performer_recommendation(job)
            job.status = "succeeded"

        except Exception as e:
            job.status = "failed"
            logging.error(
                "Dispatch for job " + job.id + " failed due to " + str(e))

        with open(processed_location, "wb") as f:
            f.write(json.dumps(job.__dict__))

        os.remove(pending_location)
        logging.info("Finished job " + job.id)
