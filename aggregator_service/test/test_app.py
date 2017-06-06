from aggregator_service import app
from unittest import TestCase

FIXTURE_PENDING_JOB_1 = "5c22b510-98ec-4570-a8e5-1c422ffb41f9"
FIXTURE_PENDING_JOB_2 = "b8e46f11-dc79-469a-92f6-0a7b4897c97f"


class TestApp(TestCase):

    def test_get_pending_jobs(self):
        jobs = app.get_pending_jobs("test/fixtures/pending-static")

        expected_jobs = [
            FIXTURE_PENDING_JOB_1,
            FIXTURE_PENDING_JOB_2
        ]

        self.assertTrue(FIXTURE_PENDING_JOB_1 in jobs)
        self.assertTrue(FIXTURE_PENDING_JOB_2 in jobs)
        self.assertTrue(2, (len(expected_jobs)))
