FROM python:3.8-slim

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    ffmpeg

RUN pip install azure-cognitiveservices-speech ffmpeg-python pymongo

RUN useradd -m -d /home/sota -s /bin/bash sota
USER sota
WORKDIR /tmp
