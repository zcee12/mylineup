# My Related Lineup

Ideally you'd extend this to build up a playlist for all the related artists.

At the moment it takes the users favourite artists as an input, looks up their related artists in the Spotify API and intersects them with the lineup of the SongKick event chosen.

You could also find the related artists for artists from the SongKick line up and increase your chance of finding overlaps.

## Running the Services

Each service will run in it's own Python virtualenv and there are dependent Make targets to install the applications dependencies first.

You'll need to install ```virtualenv``` first if you don't have it.

e.g. 
```
sudo pip install virtualenv
```

Make sure you start cleanly:
```
make clean
```

On starting the below you'll need a `runtime/` directory at the top level.
The make targets will make this for you.
It contains 'pending/' and 'processed/' directories to mimic a poor mans dispatch queue and backend.

### Run the API server
From the top level directory:
```
make run-api-server
```

### Run the Aggregator Service
From the top level directory:
```
make run-aggregator-service
```


## Running the tests
