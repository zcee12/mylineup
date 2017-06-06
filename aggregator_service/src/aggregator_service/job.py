class Job(object):

    def __init__(self, event_id, artists):
        self.status = "pending"
        self.event_id = event_id
        self.artists = artists
