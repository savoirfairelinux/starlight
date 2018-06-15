FROM python:3-alpine
FROM node:carbon-alpine AS build

FROM ubuntu
RUN apt-get update && apt-get install -y python3-pip

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY ./ /code/



RUN apt-get update
RUN apt-get install curl gettext -y
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install nodejs build-essential -y
RUN apt-get install binutils libproj-dev gdal-bin -y
RUN apt-get clean

RUN pip3 install -r requirements.txt


RUN npm install
RUN rm -rf /code/demo/static/build
RUN npm install webpack-cli
RUN npm run webpack
