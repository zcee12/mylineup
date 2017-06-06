import os
import json
from mock import Mock
from unittest import TestCase
from aggregator_service.job import Job
from aggregator_service.processor import Processor

JOB_ID = "5c22b510-98ec-4570-a8e5-1c422ffb41f9"
FIXTURE_JOB = (
    "test/fixtures/pending/5c22b510-98ec-4570-a8e5-1c422ffb41f9")
EXPECTED_JOB = (
    "test/fixtures/processed/5c22b510-98ec-4570-a8e5-1c422ffb41f9")
PROCESSED_DIR = "test/fixtures/processed"


class TestProcessor(TestCase):

    def setUp(self):
        self.spotify_client = Mock()
        self.songkick_client = Mock()
        self.processor = Processor(
            PROCESSED_DIR,
            self.spotify_client,
            self.songkick_client
        )
        self.job = Job(JOB_ID, "123", ["Radiohead", "Ed Sheeran"])

        # TODO: Mock out the file IO rather than making destructive actions
        try:
            os.remove(EXPECTED_JOB)
        except (OSError):
            pass

    def test_init(self):
        self.assertEquals(
            PROCESSED_DIR, self.processor.processed_dir)
        self.assertEquals(self.spotify_client, self.processor.spotify_client)
        self.assertEquals(self.songkick_client, self.processor.songkick_client)

    def test_dispatch_fails_job_for_spotify_client_exception(self):
        self.spotify_client.get_artist_uri = Exception
        try:
            self.processor.dispatch(self.job)
            self.fail()

        except Exception:
            with open(EXPECTED_JOB) as f:
                job = json.loads(f.read())
            self.assertEquals("failed", job["status"])

    def test_dispatch_fails_job_for_songkick_client_exception(self):
        self.spotify_client.get_performers = Exception
        try:
            self.processor.dispatch(self.job)
            self.fail()

        except Exception:
            with open(EXPECTED_JOB) as f:
                job = json.loads(f.read())
            self.assertEquals("failed", job["status"])

    def test_dispatch_success(self):
        pass
