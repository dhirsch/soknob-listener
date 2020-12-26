# soknob-listener
Sonos controller listening server

docker run \
    -it --rm \
    --mount type=bind,source="$(pwd)"/sonos.json,target=/app/sonos.json \
    soknob-listener:latest