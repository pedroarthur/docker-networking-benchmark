#!/bin/bash

output="${1?I need a file to save output to}"

docker ps -f label=experiment.sink=true -q | while read -r image
do
  docker logs -t "$image" | tee "$output-96-4-$image.logs"
done

