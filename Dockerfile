FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install libpq-dev gcc
COPY ./requirements.txt /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./ /app

RUN pip install -r /requirements.txt

CMD python app.py
