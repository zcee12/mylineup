import os
import uuid
from flask import Flask, request, Response, json
app = Flask(__name__)


# TODO pass this in at runtime
PENDING_DIR = "test/fixtures/pending"
PROCESSED_DIR = "test/fixtures/processed"


class ValidationError(Exception):
    pass


def _get_processed_location(lineup):
    return os.path.join(PROCESSED_DIR, lineup)


def _is_pending(lineup):
    pending_location = os.path.join(PENDING_DIR, lineup)
    return os.path.isfile(pending_location)


def _is_processed(lineup):
    return os.path.isfile(_get_processed_location(lineup))


def _get_processed_status(lineup):
    with open(_get_processed_location(lineup)) as f:
        job = json.loads(f.read())
    return job["status"]


def write_job(path, data):
    with open(path, "wb") as f:
        f.write(data)


def validate(data):
    # TODO Switch to using jsonschema if this gets more complicated
    try:
        event_id = request.json["event_id"]
        artists = request.json["artists"]
    except KeyError:
        raise ValidationError("JSON body does not match schema")

    try:
        # TODO Make this sane
        assert type(event_id) == type(unicode())
        assert type(artists) == type(list())

    except AssertionError:
        raise ValidationError("JSON body does not match schema")


@app.errorhandler(ValidationError)
def bad_request(error):
    return Response(
        json.dumps({"status": 400}),
        status=400,
        mimetype="application/json"
    )


@app.route("/api/v1/lineup/recommend", methods=["POST"])
def recommend():
    validate(request.json)

    job = os.path.join(PENDING_DIR, str(uuid.uuid4()))
    with open(job, "wb") as f:
        f.write(json.dumps(request.json))

    data = json.dumps({"ref": "/api/v1/lineup/1"})
    return Response(data, status=201, mimetype="application/json")


@app.route("/api/v1/lineup/<lineup>/status")
def status(lineup):

    if _is_processed(lineup):
        status = _get_processed_status(lineup)
        return Response(
            json.dumps({"value": status}),
            status=200,
            mimetype="application/json"
        )

    if _is_pending(lineup):
        return Response(
            json.dumps({"value": "pending"}),
            status=200,
            mimetype="application/json"
        )

    return Response(
        json.dumps({"msg": "Line up not found"}),
        status=404,
        mimetype="application/json"
    )


@app.route("/api/v1/lineup/<_id>")
def lineup(_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
