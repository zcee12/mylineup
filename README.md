# My Lineup
Takes a list of artists, finds their related artists (using Spotify) and recommends a lineup for a particular event (described by SongKick). e.g. A Festival.

Ideally you'd extend this to build up a playlist for all the related artists.
You could also collect related artists for artists from the SongKick line up and increase your chance of finding overlaps.

## Running the Services

All commands are assumed to be from the project root.
Some change into sub directories - make sure you return to the root to run the next command.

### Credentials
You need both Spotify and Songkick API keys.
Create a config file under ```aggregator_service/config.json```

Provide key value pairs for the API keys (dropping in your own keys):
```
{
    "spotify_client_id": "<spotify-client-id>",
    "spotify_client_secret": "<spotify-client-secret>",
    "songkick_api_key": "<songkick-api-key>"
}
```

### Environment
The services are built against Python2.7.

Each service will run in it's own Python ```virtualenv```; there are dependent Make targets to install each applications dependencies first.

You *will* need to install ```virtualenv``` if you don't have it. 

e.g. 
```
pip install virtualenv
```
You may need to provide sudo.

### Start cleanly
Make sure you start cleanly:
```
make clean
```

### Note on Runtime directories
On starting the below you'll need a `runtime/` directory at the top level.
The make targets should take care of this for you.
The runtime directory contains ```pending/``` and ```processed/``` directories to mimic a poor mans dispatch queue and backend.
Both services require "PENDING_DIR" and "PROCESSING_DIR" to be set as environment variables. If you use the make targets, these will be set for you.

### Run the API server
From the top level directory:
```
make run-api-server
```
It should appear on localhost:5000.

### Run the Aggregator Service
From the top level directory:
```
make run-aggregator-service
```


## Run the acceptance / sanity-test
You can run an end to end by running:
```
cd acceptance && make test
```

Or just call the /recommend API with some sample data and follow the links through yourself:
```
make sanity-check
```

## The API

### Ask for a lineup recommendation
*Request*

```
POST /api/v1/lineup/recommend
Content-Type: application/json

{
    "event_id": "27082564-glastonbury-festival-2017",
    "artists": ["Radiohead", "Muse"]
}
```
*event_id* is a valid SongKick event ID.
- See https://www.songkick.com/developer/events-details

*artists* is a list valid Spotify artist names.
- (My intention was to use the top artists for a particular user and pass these straight in.)

*Response*
```
Content-Type: application/json

{
    "ref": "http://localhost:5000/api/v1/lineup/04bdea20-968e-49af-900b-16566fa5d61f"
}
```

### Check the status of a lineup being built
*Request*
```
GET http://localhost:5000/api/v1/lineup/04bdea20-968e-49af-900b-16566fa5d61f/status
```

*Response*
```
Content-Type: application/json

{
    "value": "pending"
}
```
*value* is one of `pending|failed|succeeded`

### List all recommended lineups (no truncation or pagination!)
*Request*
```
GET http://localhost:5000/api/v1/lineup
```

*Response*
```
[
  "http://localhost:5000/api/v1/lineup/dc25ce0d-11e9-430f-9eb7-b54fe9c57842",
  "http://localhost:5000/api/v1/lineup/60074416-622d-45c5-b1c8-c0cd86511098"
]
```

### Get a recommended lineup
*Request*

```
GET http://localhost:5000/api/v1/lineup/04bdea20-968e-49af-900b-16566fa5d61f
```

*Response*
```
{
    artists: [
        "Radiohead",
        "Muse"
    ],
    event_id: "27082564-glastonbury-festival-2017",
    result: [
        "Biffy Clyro",
        "The Flaming Lips",
        "Radiohead",
        "Nothing But Thieves"
    ],
    status: "succeeded"
}
```

## Unit and Integration Tests

### api-server
You'll need to first start the service in a separate process with a test set of directories:
```
cd api_server && make run-for-test
```
(Make sure you've stopped any previously started api servers on port 5000)

Then...
```
cd api_server && make test
```

### aggregator-service
```
cd aggregator_service && make test
```
