FROM python:3.7-alpine
LABEL maintainer "mi2428 <tmiya@protonmail.ch>"

ENV LANG C.UTF-8
WORKDIR /app

RUN apk --no-cache add curl

COPY ./src/Pipfile .
COPY ./src/Pipfile.lock .
RUN pip install pipenv \
 && pipenv install system

COPY ./src .
CMD ["pipenv", "run", "notifier"]
