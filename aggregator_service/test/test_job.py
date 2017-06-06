from unittest import TestCase
from aggregator_service.job import Job, job_from


class TestJob(TestCase):

    def setUp(self):
        self.job = Job(
            "uuid",
            "27082564-glastonbury-festival-2018",
            ["Radiohead", "Ed Sheeran"]
        )

    def test_init(self):
        self.assertEquals("uuid", self.job.id)
        self.assertEquals(
            "27082564-glastonbury-festival-2018", self.job.event_id)
        self.assertEquals(["Radiohead", "Ed Sheeran"], self.job.artists)
        self.assertEquals("pending", self.job.status)
        self.assertEquals(None, self.job.result)

    def test_from(self):
        job = job_from(
            "5c22b510-98ec-4570-a8e5-1c422ffb41f9",
            "test/fixtures/pending-static"
        )
        self.assertEquals("5c22b510-98ec-4570-a8e5-1c422ffb41f9", job.id)
        self.assertEquals("27082564-glastonbury-festival-2018", job.event_id)
        self.assertEquals(["Radiohead", "Ed Sheeran"], job.artists)
