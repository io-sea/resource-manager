# syntax=docker/dockerfile:1

FROM python:3.10-slim

WORKDIR /RM

RUN apt-get -y update
RUN apt-get -y install nano

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /RM/src/resource_manager

CMD gunicorn  --worker-class gevent --workers 1 --bind 0.0.0.0:5000 run:app --max-requests 10000


