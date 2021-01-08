import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)

server.config.from_object(os.environ['APP_SETTINGS'])
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

from move import bp
from stats import stats_bp

server.register_blueprint(bp)
server.register_blueprint(stats_bp)


@server.route('/')
def hello_world():
    return render_template('mandi.html')
