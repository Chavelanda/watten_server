from flask import Flask
from move import bp

server = Flask(__name__)

server.register_blueprint(bp)

@server.route('/')
def hello_world():
    return 'hello world!'
