#!/bin/bash

docker ps -f "label=experiment.${1:-sink}=true" -q | parallel -l1 --line-buffer docker logs -t -f

