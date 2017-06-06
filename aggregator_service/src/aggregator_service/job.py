class Job(object):

    def __init__(self, id, event_id, artists):
        self.id = id
        self.status = "pending"
        self.event_id = event_id
        self.artists = artists
        self.result = None
