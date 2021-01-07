# WATTEN SERVER

## Introduction

Watten server is an application developed to serve a [Watten](https://en.wikipedia.org/wiki/Watten_(card_game)) game client. It has two main functions:

- Given a state of the game and a difficulty level, it returns the best action to take based on a model related to the above mentioned difficulty level;
- It is possible to insert and retrieve statistics of the game played against each difficulty level player.

To learn more about this project take a look at the [mobile application](https://github.com/Chavelanda/watten_app) or at the [thesis project](https://github.com/Chavelanda/offen-watten-alpha-zero) aiming at applying an AlphaZero approach to Watten.

This server is a dockerized application implemented with Flask and communicating with a Postgres database. 

## Get started

The files *database.env*, *.env* and *docker-compose.yml* are only needed for running the server locally.

##### docker-compose.yml

In the docker-compose.yml file we define two services: the web application (Flask app) and the database. For each of these service we have the correspondent environments variables written in the *.env files. The entrypoinst.sh file defines the commands that have to be run when building the application, i.e. initializing the db and then running the app.

```yaml
version: '3.9'
services:
  web:
    build: .
    entrypoint: /entrypoint.sh
    ports:
      - "5000:5000"
    env_file: .env
    depends_on:
      - db
    volumes:
      - .:/opt/webapp
  db:
    image: postgres:latest
    ports:
      - "5432:5432"
    env_file: database.env

```

The web service itself is bulit using the Dockerfile at the project Root:

```dockerfile
FROM python:3.6

WORKDIR usr/src/flask_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 5000

COPY . .

ENV  APP_SETTINGS="config.ProductionConfig"

CMD gunicorn --bind 0.0.0.0:$PORT wsgi:server

```

The Dockerfile contains the instructions to install the requirements of the app, makes the entrypoint.sh file executable, exposes port 5000 (only needed for local running), sets the environment variables (needed for heroku deployment) and run the app from (only for heroku deployment, locally commands tu run the app are set in entrypoint.sh)

## Run locally

In order to run the application locally you must have installed docker and docker-compose.

Run the command

```bash
docker compose-up
```

The app will start at http://localhost:5000/. By clicking the link you should see a simple *hello world!* text.

## Deploy to heroku

In order to deploy the application to heroku you must have installed heroku-cli and docker.

Login to container registry

```bash
heroku container:login
```

Create the heroku application

```bash
heroku create name_of_your_app
```

Add Postgres addon to heroku

```shell
heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application
```

Push the web image to heroku

```shell
heroku container:push web
```

Release the application

```shell
heroku container:release web
```

Open it, you should get the usual *hello world!* answer

```shell
heroku open
```

Heroku will automatically set the environment variables $PORT and $DATABASE_URL.

Before the application can really work you have to initialize the database and run the migrations.

In order to do this first run bash in your heroku app.

```shell
heroku run bash
```

Then make the init_db.sh file executable

```bash
chmod +x init_db.sh
```

Finally run the init_db.sh bash file

```bash
./init_db.sh
```

Exit the bash. Now the database is initialized.