# fuchur-bot

Welcome bot for the Dragonscale Castle Chat

## How I'd deploy

1. Build a new image
`sudo docker build -t fuchur .`
1. Stop the current container
`sudo docker container stop fuchur`
1. Remove the current container
`sudo docker container rm fuchur`
1. Run the new image
`sudo docker run --restart always -d --name fuchur fuchur`
