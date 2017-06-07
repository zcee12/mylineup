import json
import requests

from time import sleep

# POST
response = requests.post(
    "http://localhost:5000/api/v1/lineup/recommend",
    headers={"Content-Type": "application/json"},
    data=json.dumps(
        {
            "event_id": "27082564-glastonbury-festival-2017",
            "artists": ["Radiohead", "Muse"]
        }
    )
)

response.raise_for_status()
print response.json()
ref = response.json()["ref"]

# Follow the ref
lineup = requests.get(ref)
lineup.raise_for_status()
print lineup

# Check the status
t = 0
done = False
while(t < 10 and not done):
    status = requests.get("{0}/status".format(ref))
    status.raise_for_status()
    value = status.json()["value"]
    print value
    if value != "pending":
        done = True
    t += 1
    sleep(1)

# Go back and check the result
lineup = requests.get(ref)
lineup.raise_for_status()
print lineup.json()

# Assert expected response
# This is poor - the APIs could change but it's a good sanity check
assert "Radiohead" in lineup.json()["result"]
assert "The Flaming Lips" in lineup.json()["result"]
assert "Biffy Clyro" in lineup.json()["result"]
assert "Nothing But Thieves" in lineup.json()["result"]
