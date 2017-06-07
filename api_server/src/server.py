import os
import uuid
from flask import Flask, request, Response, json
app = Flask(__name__)


class ValidationError(Exception):
    pass


@app.errorhandler(ValidationError)
def bad_request(error):
    return Response(
        json.dumps({"status": 400}),
        status=400,
        mimetype="application/json"
    )

PENDING_DIR = "test/fixtures/pending"


def write_job(path, data):
    with open(path, "wb") as f:
        f.write(data)


def validate(data):
    # TODO Switch to using jsonschema if this gets more complicated
    try:
        event_id = request.json["event_id"]
        artists = request.json["artists"]
        print event_id
    except KeyError:
        raise ValidationError("JSON body does not match schema")

    try:
        print type(event_id)
        # TODO Make this sane
        assert type(event_id) == type(unicode())
        assert type(artists) == type(list())

    except AssertionError:
        raise ValidationError("JSON body does not match schema")


@app.route("/api/v1/lineup/recommend", methods=["POST"])
def recommend():
    validate(request.json)

    job = os.path.join(PENDING_DIR, str(uuid.uuid4()))
    with open(job, "wb") as f:
        f.write(json.dumps(request.json))
    data = json.dumps({"ref": "/api/v1/lineup/1"})
    return Response(data, status=201, mimetype="application/json")


@app.route("/api/v1/lineup/<id>/status")
def status(_id):
    pass


@app.route("/api/v1/lineup/<_id>")
def lineup(_id):
    pass

if __name__ == "__main__":
    app.run(debug=True)
