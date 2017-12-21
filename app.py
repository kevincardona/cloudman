from gevent import monkey
monkey.patch_all()
from flask import Flask
from gevent import wsgi

import requests
import server_config

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index ():
    return "Hello World"

server = wsgi.WSGIServer((server_config.SERVER_IP, server_config.SERVER_PORT), app)
server.serve_forever()
