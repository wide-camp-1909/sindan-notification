FROM python:3.7-alpine
LABEL maintainer "mi2428 <tmiya@protonmail.ch>"

ENV LANG C.UTF-8
WORKDIR /app

COPY ./src .
RUN pip install pipenv \
 && pipenv install --system

CMD ["python", "./notifier.py"]
