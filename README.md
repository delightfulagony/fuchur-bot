# fuchur-bot

Welcome bot for the Dragonscale Castle Chat

This telegram bot greets an user with a message (allowing for translation), and
links them to a different manager (*tutor* in the context of the game).

It also includes a some interactions where fuchur asks players to scratch their
ear.

## How I'd deploy

1. Build a new image
`sudo docker build -t fuchur .`
1. Stop the current container
`sudo docker container stop fuchur`
1. Remove the current container
`sudo docker container rm fuchur`
1. Run the new image
`sudo docker run --restart always -d --name fuchur fuchur`

## tutors.txt

This file holds links to the tutor's accounts. Each line should be a separate
link.
