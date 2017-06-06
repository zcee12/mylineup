import os
import json


class Job(object):

    def __init__(self, id, event_id, artists):
        self.id = id
        self.status = "pending"
        self.event_id = event_id
        self.artists = artists
        self.result = None


def job_from(_id, _dir):
    path = os.path.join(_dir, _id)
    with open(path) as f:
        data = json.loads(f.read())
        return Job(
            _id,
            data["event_id"],
            data["artists"]
        )
