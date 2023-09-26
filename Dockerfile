# pull official base image
# FROM nikolaik/python-nodejs:python3.11-nodejs18-bullseye
FROM python:3.11.4-bullseye

# set work directory
COPY . /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements_dev.txt .

RUN apt-get update
RUN apt-get install -y binutils libproj-dev

RUN pip install --upgrade pip
RUN pip install -r requirements_dev.txt

# copy entrypoint.sh
COPY ./docker-entrypoint.sh .
RUN sed -i 's/\r$//g' /app/docker-entrypoint.sh
RUN chmod a+x /app/docker-entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
