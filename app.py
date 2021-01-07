import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from move import bp
from stats import stats_bp

server = Flask(__name__)

server.config.from_object(os.environ['APP_SETTINGS'])
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

server.register_blueprint(bp)
server.register_blueprint(stats_bp)


@server.route('/')
def hello_world():
    return 'hello world!'
