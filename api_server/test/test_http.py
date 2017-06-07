import os
import shutil
import json
import uuid
import requests
from unittest import TestCase


PENDING_DIR = "test/fixtures/pending"
PROCESSED_DIR = "test/fixtures/processed"
BASE_URL = "http://localhost:5000/api/v1"


def clean():
    try:
        shutil.rmtree(PENDING_DIR)
        shutil.rmtree(PROCESSED_DIR)
    except OSError:
        pass


class BaseCase(TestCase):

    def setUp(self):
        clean()
        # TODO: force creation of intermediates
        os.mkdir(PENDING_DIR)
        os.mkdir(PROCESSED_DIR)

    def tearDown(self):
        clean()


class TestRecommendEndpoint(BaseCase):

    def test_success(self):
        event_id = str(uuid.uuid4())
        payload = {
            "event_id": event_id,
            "artists": ["Muse", "Radiohead"]
        }

        url = build("/lineup/recommend")
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        self.assertEqual(201, response.status_code)
        self.assertTrue("/api/v1/lineup/" in response.json()["ref"])
        self.assertFalse(len(response.json()["ref"].rsplit("/")[-1]) == 0)

        job = os.listdir(PENDING_DIR)[0]
        expected_location = os.path.join(PENDING_DIR, job)

        with open(expected_location) as f:
            data = json.loads(f.read())
            # TODO Test for valid uuid4 id
            self.assertEquals(event_id, data["event_id"])
            self.assertEquals(
                sorted(["Muse", "Radiohead"]), sorted(data["artists"])
            )

    def test_invalid_json_returns_400(self):
        url = build("/lineup/recommend")
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data="/"
        )

        self.assertEqual(400, response.status_code)

    def test_no_event_id_field_returns_400(self):
        payload = {
            "artists": ["Muse", "Radiohead"]
        }

        url = build("/lineup/recommend")
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        self.assertEqual(400, response.status_code)

    def test_event_id_not_string_returns_400(self):
        payload = {
            "event_id": 2,
            "artists": ["Muse", "Radiohead"]
        }

        url = build("/lineup/recommend")
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        self.assertEqual(400, response.status_code)

    def test_no_artists_field_returns_400(self):
        payload = {
            "event_id": "123"
        }

        url = build("/lineup/recommend")
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        self.assertEqual(400, response.status_code)

    def test_artists_not_list_returns_400(self):
        payload = {
            "event_id": "123",
            "artists": "Muse"
        }

        url = build("/lineup/recommend")
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        self.assertEqual(400, response.status_code)

#    def test_no_content_type(self):
#        payload = {
#            "event_id": "123",
#            "artists": ["Muse", "Radiohead"]
#        }
#
#        url = build("/lineup/recommend")
#        response = requests.post(
#            url,
#            headers={"Content-Type": "application/json"},
#            data=json.dumps(payload)
#        )
#
#        self.assertEqual(400, response.status_code)


class TestLineUpStatusEndpoint(BaseCase):

    def test_not_found_returns_400(self):
        response = requests.get(build("/lineup/123-abc/status"))
        self.assertEquals(404, response.status_code)
        self.assertEquals("Line up not found", response.json()["msg"])

    def test_pending(self):
        with open(os.path.join(PENDING_DIR, "123-abc"), "wb") as f:
            f.write("{}")

        response = requests.get(build("/lineup/123-abc/status"))
        self.assertEquals(200, response.status_code)
        self.assertEquals({"value": "pending"}, response.json())

    def test_processed_and_failed_returns(self):
        with open(os.path.join(PROCESSED_DIR, "123-abc"), "wb") as f:
            f.write(json.dumps({"status": "failed"}))

        response = requests.get(build("/lineup/123-abc/status"))
        self.assertEquals(200, response.status_code)
        self.assertEquals({"value": "failed"}, response.json())

    def test_processed_and_succeeded_returns(self):
        with open(os.path.join(PROCESSED_DIR, "123-abc"), "wb") as f:
            f.write(json.dumps({"status": "succeeded"}))

        response = requests.get(build("/lineup/123-abc/status"))
        self.assertEquals(200, response.status_code)
        self.assertEquals({"value": "succeeded"}, response.json())

    def test_processed_before_removing_from_pending_returns(self):
        with open(os.path.join(PROCESSED_DIR, "123-abc"), "wb") as f:
            f.write(json.dumps({"status": "succeeded"}))

        with open(os.path.join(PENDING_DIR, "123-abc"), "wb") as f:
            f.write("{}")

        response = requests.get(build("/lineup/123-abc/status"))
        self.assertEquals(200, response.status_code)
        self.assertEquals({"value": "succeeded"}, response.json())


class TestLineUpEndpoint(BaseCase):

    def test_not_found_returns_400(self):
        response = requests.get(build("/lineup/123-abc/status"))
        self.assertEquals(404, response.status_code)
        self.assertEquals("Line up not found", response.json()["msg"])

    def test_successful_result_returns(self):
        # Maybe we should just serialize the actual Job object here instead?
        successful_job = {
            "id": "123-abc",
            "status": "succeeded",
            "event_id": "Glastonbury-2017",
            "artists": ["Radiohead", "Nobody"],
            "result": ["Radiohead", "Ed Sheeran"]
        }

        with open(os.path.join(PROCESSED_DIR, "123-abc"), "wb") as f:
            f.write(json.dumps(successful_job))

        response = requests.get(build("/lineup/123-abc"))
        self.assertEquals(200, response.status_code)

        r = response.json()
        self.assertEquals(4, len(r.keys()))
        self.assertEquals("succeeded", r["status"])
        self.assertEquals("Glastonbury-2017", r["event_id"])
        self.assertEquals(
            sorted(["Radiohead", "Nobody"]), sorted(r["artists"]))
        self.assertEquals(
            sorted(["Radiohead", "Ed Sheeran"]), sorted(r["result"]))

    def test_successful_empty_result(self):
        successful_job = {
            "id": "123-abc",
            "status": "succeeded",
            "event_id": "Glastonbury-2017",
            "artists": ["Radiohead", "Nobody"],
            "result": []
        }

        with open(os.path.join(PROCESSED_DIR, "123-abc"), "wb") as f:
            f.write(json.dumps(successful_job))

        response = requests.get(build("/lineup/123-abc"))
        self.assertEquals(200, response.status_code)

        r = response.json()
        self.assertEquals(4, len(r.keys()))
        self.assertEquals("succeeded", r["status"])
        self.assertEquals("Glastonbury-2017", r["event_id"])
        self.assertEquals(
            sorted(["Radiohead", "Nobody"]), sorted(r["artists"]))
        self.assertEquals([], r["result"])

    def test_failed_result_returns_none(self):
        failed_job = {
            "id": "123-abc",
            "status": "failed",
            "event_id": "Glastonbury-2017",
            "artists": ["Radiohead", "Nobody"],
            "result": None
        }

        with open(os.path.join(PROCESSED_DIR, "123-abc"), "wb") as f:
            f.write(json.dumps(failed_job))

        response = requests.get(build("/lineup/123-abc"))
        self.assertEquals(200, response.status_code)

        r = response.json()
        self.assertEquals(4, len(r.keys()))
        self.assertEquals("failed", r["status"])
        self.assertEquals("Glastonbury-2017", r["event_id"])
        self.assertEquals(
            sorted(["Radiohead", "Nobody"]), sorted(r["artists"]))
        self.assertEquals(None, r["result"])

    def test_pending_result_returns_none(self):
        pending_job = {
            "event_id": "Glastonbury-2017",
            "artists": ["Radiohead", "Nobody"],
        }

        with open(os.path.join(PENDING_DIR, "123-abc"), "wb") as f:
            f.write(json.dumps(pending_job))

        response = requests.get(build("/lineup/123-abc"))
        self.assertEquals(200, response.status_code)

        r = response.json()
        self.assertEquals(4, len(r.keys()))
        self.assertEquals("succeeded", r["status"])
        self.assertEquals("Glastonbury-2017", r["event_id"])
        self.assertEquals(
            sorted(["Radiohead", "Nobody"]), sorted(r["artists"]))
        self.assertEquals(None, r["result"])

    def test_processed_when_pending_still_exists(self):
        pending_job = {
            "event_id": "Glastonbury-2017",
            "artists": ["Radiohead", "Nobody"],
        }

        successful_job = {
            "id": "123-abc",
            "status": "succeeded",
            "event_id": "Glastonbury-2017",
            "artists": ["Radiohead", "Nobody"],
            "result": ["Radiohead", "Ed Sheeran"]
        }

        with open(os.path.join(PENDING_DIR, "123-abc"), "wb") as f:
            f.write(json.dumps(pending_job))

        with open(os.path.join(PROCESSED_DIR, "123-abc"), "wb") as f:
            f.write(json.dumps(successful_job))

        response = requests.get(build("/lineup/123-abc"))
        self.assertEquals(200, response.status_code)

        r = response.json()
        self.assertEquals(4, len(r.keys()))
        self.assertEquals("succeeded", r["status"])
        self.assertEquals("Glastonbury-2017", r["event_id"])
        self.assertEquals(
            sorted(["Radiohead", "Nobody"]), sorted(r["artists"]))
        self.assertEquals(
            sorted(["Radiohead", "Ed Sheeran"]), sorted(r["result"]))


def build(stub):
    return "{0}{1}".format(BASE_URL, stub)
