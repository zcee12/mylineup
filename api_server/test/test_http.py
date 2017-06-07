import os
import shutil
import json
import uuid
import requests
from unittest import TestCase


PENDING_DIR = "test/fixtures/pending"
BASE_URL = "http://localhost:5000/api/v1"


def clean():
    try:
        shutil.rmtree("test/fixtures/pending/")
    except OSError:
        pass


class BaseCase(TestCase):

    def setUp(self):
        clean()
        os.mkdir(PENDING_DIR)

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
        print job
        with open(os.path.join(PENDING_DIR, job)) as f:
            data = json.loads(f.read())
            print "data"
            print data
            self.assertEquals(event_id, data["event_id"])
            self.assertEquals(
                sorted(["Muse", "Radiohead"]), sorted(data["artists"])
            )

    def test_invalid_json(self):
        url = build("/lineup/recommend")
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data="/"
        )

        self.assertEqual(400, response.status_code)

    def test_no_event_id_field_throws_400(self):
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

    def test_event_id_not_string_throws_400(self):
        pass

    def test_no_artists_field_throws_400(self):
        pass

    def test_artists_not_list_throws_400(self):
        pass

    def test_no_content_type(self):
        pass


class TestLineUpStatusEndpoint(BaseCase):

    def test_pending(self):
        pass

    def test_processed(self):
        pass

    def test_not_found(self):
        pass


class TestLineUpEndpoint(BaseCase):

    def test_successful_result(self):
        pass

    def test_failed_result(self):
        pass

    def test_not_found(self):
        pass


def build(stub):
    return "{0}{1}".format(BASE_URL, stub)
