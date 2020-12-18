# WATTEN SERVER

## Steps to launch the app (Windows)

To launch the application so that is visible only in local host do the following:

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

If you want too launch the application so that is visible in LAN (not for production) substitute step 4 with the following:

4.b) Search the IPv4 address with *ipconfig*

5.b) Run the application specifying the host (https://stackoverflow.com/questions/7023052/configure-flask-dev-server-to-be-visible-across-the-network)

```
flask run --host=192.168.x.x
```

