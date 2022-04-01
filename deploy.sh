#!/bin/bash
# Build a new image
sudo docker build -t fuchur .
# Stop the current container
sudo docker container stop fuchur
# Remove the current container
sudo docker container rm fuchur
# Run the new image
sudo docker run --restart always -d --name fuchur fuchur
