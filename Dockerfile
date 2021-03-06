# pull official base image
FROM node:13.12.0-alpine as fe

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY ./book_frontend/package.json ./book_frontend/yarn.lock ./

RUN yarn install --silent 

COPY ./book_frontend/ ./

RUN yarn build

#tensorflow
FROM tensorflow/tensorflow:latest as te
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
COPY ./book_site/requirements.txt .
COPY ./book_site/requirements_tensorflow.txt .

RUN pip install -r requirements_tensorflow.txt
RUN pip install -r requirements.txt
RUN python -m spacy download en

#backend
#FROM python:3.8.3-alpine
#COPY --from=te /usr/src/app/ /usr/local/lib/python3.8/site-packages

#WORKDIR /usr/src/app
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

#RUN pip install --upgrade pip
#COPY ./book_site/requirements.txt .
#
#RUN \
# apk add --no-cache bash && \
# apk update && \
# apk add --no-cache postgresql-libs && \
# apk add --no-cache jpeg-dev zlib-dev && \
# apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
# python3 -m pip install -r requirements.txt --no-cache-dir && \
# apk --purge del .build-deps
#
#
#RUN pip install -r requirements.txt

COPY ./book_site/misc/download_nltk.py .
RUN python download_nltk.py
COPY ./book_site/ ./
COPY ./models/ /usr/

RUN chmod +x ./wait-for-it.sh
COPY --from=fe ./app/build ./frontend/build

