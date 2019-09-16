FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./Pipfile /usr/src/app/Pipfile
COPY ./Pipfile.lock /usr/src/app/Pipfile.lock
RUN pip install pipenv
RUN pipenv install --system

COPY . /usr/src/app

