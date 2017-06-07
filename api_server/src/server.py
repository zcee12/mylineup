import os
import uuid
from flask import Flask, request, Response, json
app = Flask(__name__)

MIME_TYPE = "application/json"

# TODO pass this in at runtime
PENDING_DIR = os.environ["PENDING_DIR"]
PROCESSED_DIR = os.environ["PROCESSED_DIR"]


class ValidationError(Exception):
    pass


def _get_pending_location(lineup):
    return os.path.join(PENDING_DIR, lineup)


def _get_processed_location(lineup):
    return os.path.join(PROCESSED_DIR, lineup)


def _is_pending(lineup):
    return os.path.isfile(_get_pending_location(lineup))


def _is_processed(lineup):
    return os.path.isfile(_get_processed_location(lineup))


def _get_pending_job(lineup):
    with open(_get_pending_location(lineup)) as f:
        job = json.loads(f.read())
    return job


def _get_processed_job(lineup):
    with open(_get_processed_location(lineup)) as f:
        job = json.loads(f.read())
    return job


def _get_processed_status(lineup):
    return _get_processed_job(lineup)["status"]


def _success_response(data, status):
    return Response(
        json.dumps(data),
        status=status,
        mimetype="application/json"
    )


def _not_found_response():
    return Response(
        json.dumps({"msg": "Line up not found"}),
        status=404,
        mimetype="application/json"
    )


def _bad_request_response(error):
    return Response(
        json.dumps({"msg": str(error)}),
        status=400,
        mimetype="application/json"
    )


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
    return _bad_request_response(error)


@app.route("/api/v1/lineup/recommend", methods=["POST"])
def recommend():
    validate(request.json)

    job = os.path.join(PENDING_DIR, str(uuid.uuid4()))
    with open(job, "wb") as f:
        f.write(json.dumps(request.json))

    data = json.dumps({"ref": "/api/v1/lineup/{0}".format(job)})
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
    return _not_found_response()


@app.route("/api/v1/lineup/<lineup>")
def lineup(lineup):
    if _is_processed(lineup):
        job = _get_processed_job(lineup)
        data = {
            "status": job["status"],
            "event_id": job["event_id"],
            "artists": job["artists"],
            "result": job["result"]
        }
        return _success_response(data, 200)

    if _is_pending(lineup):
        job = _get_pending_job(lineup)
        data = {
            "status": "pending",
            "event_id": job["event_id"],
            "artists": job["artists"],
            "result": None
        }
        return _success_response(data, 200)

    return _not_found_response()


if __name__ == "__main__":
    print "Starting!\n\n"
    print "Using " + PENDING_DIR + " as the job pending dir"
    print "Using " + PROCESSED_DIR + " as the job processed dir"
    print "\n\n"

    app.run(debug=True)
