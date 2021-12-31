# syntax = docker/dockerfile:1.2
FROM python:3.8.2

COPY . /srv/mock

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
