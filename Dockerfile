
FROM python:3.9.10-slim-buster

RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src
RUN apt update
RUN apt install postgresql postgresql-contrib -y

RUN pip install -r requirements.txt
COPY . /src



