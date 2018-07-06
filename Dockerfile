FROM python:3-alpine

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY ./ /code/

RUN apk add --no-cache make nodejs postgresql-dev gcc python3-dev\
  musl-dev gcc g++ python && \
  npm install --lts --silent && \
  apk del make g++ python

RUN pip3 install -r requirements.txt

RUN npm install semantic-ui
RUN rm -rf /code/starlight/static/build
RUN npm rebuild node-sass
RUN npm run webpack
