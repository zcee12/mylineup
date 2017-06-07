import os
import glob
import uuid
from sets import Set
from flask import Flask, request, Response, json, url_for
app = Flask(__name__)

MIME_TYPE = "application/json"

# This is a bit ugly :(
PENDING_DIR = os.environ["PENDING_DIR"]
PROCESSED_DIR = os.environ["PROCESSED_DIR"]


class ValidationError(Exception):
    pass


def _list_just_job_ids(directory):
    relative_paths = glob.glob(os.path.join(directory, "*"))
    return [rp.split("/")[-1] for rp in relative_paths]


def _get_pending_job_ids():
    return _list_just_job_ids(PENDING_DIR)


def _get_processed_job_ids():
    return _list_just_job_ids(PROCESSED_DIR)


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
        assert type(event_id) is unicode
        assert type(artists) is list

    except AssertionError:
        raise ValidationError("JSON body does not match schema")


@app.errorhandler(ValidationError)
def bad_request(error):
    return _bad_request_response(error)


@app.route("/api/v1/lineup/recommend", methods=["POST"])
def recommend():
    validate(request.json)

    job_id = str(uuid.uuid4())

    job = os.path.join(PENDING_DIR, job_id)
    with open(job, "wb") as f:
        f.write(json.dumps(request.json))

    data = json.dumps(
        {"ref": url_for("lineup", lineup=job_id, _external=True)})
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


@app.route("/api/v1/lineup")
def lineups():
    pending = _get_pending_job_ids()
    processed = _get_processed_job_ids()

    lineups = list(Set(pending).union(Set(processed)))

    refs = [url_for("lineup", lineup=l, _external=True) for l in lineups]
    return _success_response(refs, 200)


if __name__ == "__main__":
    print "Starting!\n\n"
    print "Using " + PENDING_DIR + " as the job pending dir"
    print "Using " + PROCESSED_DIR + " as the job processed dir"
    print "\n\n"

    app.run(debug=True)
