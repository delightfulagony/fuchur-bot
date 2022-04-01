# Base image
FROM python:latest

# Workdir
RUN mkdir /app
ADD . /app
WORKDIR /app

# Dependencies
RUN pip install -r ./requirements.txt

# Run the bot
CMD python /app/fuchur.py

