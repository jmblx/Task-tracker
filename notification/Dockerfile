FROM python:3.11-slim-buster

RUN mkdir /notification_app

WORKDIR /notification_app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH=/usr/src

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

COPY / .

RUN chmod a+x docker/*.sh