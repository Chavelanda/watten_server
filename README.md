# WATTEN SERVER

## Introduction

Watten server is an application developed to serve a [Watten](https://en.wikipedia.org/wiki/Watten_(card_game)) game client. It has two main functions:

- Given a state of the game and a difficulty level, it returns the best action to take based on a model related to the above mentioned difficulty level;
- It is possible to insert and retrieve statistics of the game played against each difficulty level player.

To learn more about this project take a look at the [mobile application](https://github.com/Chavelanda/watten_app) or at the [thesis project](https://github.com/Chavelanda/offen-watten-alpha-zero) aiming at applying an AlphaZero approach to Watten.

## Get started (windows)

#### To launch the application so that is visible only in local host do the following:

1) Set where to find the application

```
set FLASK_APP=app.py
```

2) Set the environment to be development

```
set FLASK_ENV=development
```

3) Switch off debug mode (compulsory otherwise tensorflow does not work https://github.com/tensorflow/tensorflow/issues/34607)

```
set FLASK_DEBUG=0
```

4) Run the application

```
flask run
```

#### If you want too launch the application so that is visible in LAN (not for production) substitute step 4 with the following:

4.b) Search the IPv4 address with *ipconfig*

5.b) Run the application specifying the host (https://stackoverflow.com/questions/7023052/configure-flask-dev-server-to-be-visible-across-the-network)

```
flask run --host=192.168.x.x
```

