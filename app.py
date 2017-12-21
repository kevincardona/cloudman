from gevent import monkey
monkey.patch_all()

import sys
import requests
import server_config

from flask import Flask, request
from gevent import wsgi

sys.path.append('routes/')
from auth import asignup, alogin, authenticate

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index ():
    test()
    return "Connected to " + server_config.SERVER_IP + "!"

@app.route("/signup", methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    return asignup(username, password)

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    return alogin(username, password)



server = wsgi.WSGIServer((server_config.SERVER_IP, server_config.SERVER_PORT), app)
server.serve_forever()
