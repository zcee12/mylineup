# Stage finder

## Request your personalised line up
POST /api/v1/lineup/provider/{provider}/build

{
}


## Poll whether it's ready
GET /api/v1/lineup/{id}/status

{
    "pending|done"
}

## Get the line up
/api/v1/lineup/{id}

{
}
