# syntax=docker/dockerfile:1
FROM rust:slim-bullseye
WORKDIR .
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip
RUN apt-get -y update; apt-get -y install curl; apt-get -y install build-essential
RUN pip install setuptools
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "bot.py"]
