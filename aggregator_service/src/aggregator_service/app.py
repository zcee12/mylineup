import os
import json
import spotipy
import logging
import sys

from time import sleep
from job import job_from
from processor import Processor
from spotipy.oauth2 import SpotifyClientCredentials
from clients.spotify import SpotifyClient
from clients.songkick import SongkickClient


LOGGER = logging.getLogger(__name__)
INTERVAL = 10
CONF_LOCATION = "config.json"

PENDING_DIRECTORY = os.environ["PENDING_DIR"]
PROCESSED_DIRECTORY = os.environ["PROCESSED_DIR"]


class Config(object):

    def __init__(self,
                 spotify_client_id,
                 spotify_client_secret,
                 songkick_api_key):
        self.spotify_client_id = spotify_client_id
        self.spotify_client_secret = spotify_client_secret
        self.songkick_api_key = songkick_api_key


def get_pending_jobs(pending_jobs_dir):
    jobs = os.listdir(pending_jobs_dir)
    return jobs


def get_spotify_client(config):
    # Set up the underlying Spotify Client
    client_credentials_manager = SpotifyClientCredentials(
        client_id=config.spotify_client_id,
        client_secret=config.spotify_client_secret
    )
    internal_client = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager
    )

    # Pass it to our wrapper
    return SpotifyClient(internal_client)


def get_songkick_client(config):
    return SongkickClient(config.songkick_api_key)


def get_credentials(conf_location):
    with open(conf_location) as f:
        data = json.loads(f.read())
        return Config(
            data["spotify_client_id"],
            data["spotify_client_secret"],
            data["songkick_api_key"]
        )


def main():
    print "started..."

    config = get_credentials(CONF_LOCATION)
    spotify_client = get_spotify_client(config)
    songkick_client = get_songkick_client(config)

    processor = Processor(
        PENDING_DIRECTORY,
        PROCESSED_DIRECTORY,
        spotify_client,
        songkick_client
    )

    while(1):
        try:
            job_ids = get_pending_jobs(PENDING_DIRECTORY)
            print "Found job ids {0}".format(job_ids)

            for job_id in job_ids:
                job = job_from(job_id, PENDING_DIRECTORY)
                processor.dispatch(job)
        except Exception as e:
            logging.error(
                "Error {0} processing job batch {1} ".format(str(e), job_ids))
        sleep(INTERVAL)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()
