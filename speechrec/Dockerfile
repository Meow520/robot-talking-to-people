FROM python:3.8-slim

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    ffmpeg \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-pulseaudio \
    libgstreamer1.0-0 \
    pulseaudio

RUN pip install azure-cognitiveservices-speech stomp.py ffmpeg-python pymongo

RUN useradd -m -d /home/sota -s /bin/bash sota
USER sota
WORKDIR /tmp
