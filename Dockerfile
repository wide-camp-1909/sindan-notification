FROM python:3.7-alpine
LABEL maintainer "mi2428 <tmiya@protonmail.ch>"

ENV LANG C.UTF-8
WORKDIR /app

COPY ./src .
RUN apk --no-cache add curl
RUN pip install pipenv \
 && pipenv install system

CMD ["pipenv", "run", "notifyer"]
