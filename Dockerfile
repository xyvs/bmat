# pull official base image
FROM python:3.7.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./test.py /usr/src/app/test.py
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install

# copy files
COPY ./ /usr/src/app/
