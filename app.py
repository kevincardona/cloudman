from gevent import monkey
monkey.patch_all()

import jwt
import json
import sys
import requests
import server_config

from flask import Flask, request, send_file
from gevent import wsgi
from functools import wraps

sys.path.append('routes/')
from auth import asignup, alogin, authenticate

app = Flask(__name__)

def requires_auth(request):
    token = request.form['token']
    if (authenticate(token) == False):
        res = { "success": False, "message": "Invalid token" }
        return json.dumps(res)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.form['token']
        if (authenticate(token) == False):
            res = { "success": False, "message": "Invalid token" }
            return json.dumps(res)
        return f(*args, **kwargs)
    return decorated


@app.route("/", methods=['GET', 'POST'])
def index ():
    test()
    return "Connected to " + server_config.SERVER_IP + "!"


# TODO: Limit username/password character use + create user storage folder
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

@app.route("/file", methods=['POST'])
@requires_auth
def files():
    token = request.form['token']
    decoded = jwt.decode(token, server_config.JWT_SECRET, server_config.JWT_ALGORITHM )
    user_dir = "storage/" + decoded['username'] + "/"

    filename = user_dir + request.form['filename']
    return send_file(filename)

@app.route("/ls", methods=['POST'])
def ls():
    print "ls"


@app.route("/mkdir", methods=['POST'])
def mkdir():
    print "mkdir"


server = wsgi.WSGIServer((server_config.SERVER_IP, server_config.SERVER_PORT), app)
server.serve_forever()
