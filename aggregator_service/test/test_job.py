from unittest import TestCase
from aggregator_service.job import Job


class TestJob(TestCase):

    def setUp(self):
        self.job = Job("uuid", "123", ["Radiohead", "Ed Sheeran"])

    def test_init(self):
        self.assertEquals("uuid", self.job.id)
        self.assertEquals("123", self.job.event_id)
        self.assertEquals(["Radiohead", "Ed Sheeran"], self.job.artists)
        self.assertEquals("pending", self.job.status)
        self.assertEquals(None, self.job.result)
