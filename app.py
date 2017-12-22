from gevent import monkey
monkey.patch_all()
import jwt, json, requests, glob, os, server_config, sys
sys.path.append('routes/')
from flask import Flask, request, send_file
from gevent import wsgi
from werkzeug.utils import secure_filename
from functools import wraps
from auth import asignup, alogin, authenticate

app = Flask(__name__)

# END OF IMPORTS + GLOBALS

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
    try:
        token = request.form['token']
        decoded = jwt.decode(token, server_config.JWT_SECRET, server_config.JWT_ALGORITHM )
        user_dir = "storage/" + decoded['username'] + "/"
        filename = user_dir + request.form['filename']
        return send_file(filename)
    except Exception:
        res = { "success": False, "message": "failed to send file" }
        return json.dumps(res)


#  TODO: clarify cur_dirs filtering capabilities
@app.route("/ls", methods=['POST'])
@requires_auth
def ls():
    try:
        token = request.form['token']
        decoded = jwt.decode(token, server_config.JWT_SECRET, server_config.JWT_ALGORITHM )
        user_dir = "storage/" + decoded['username'] + "/"
        current_dir = user_dir + request.form['cur_dir'] + "*"
    except Exception:
        res = { "success": False, "message": "failed to ls" }
        return json.dumps(res)
    return json.dumps(glob.glob(current_dir))


@app.route("/mkdir", methods=['POST'])
@requires_auth
def mkdir():
    try:
        token = request.form['token']
        decoded = jwt.decode(token, server_config.JWT_SECRET, server_config.JWT_ALGORITHM )
        user_dir = "storage/" + decoded['username'] + "/"
        new_dir = user_dir + request.form['new_dir']
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
    except Exception:
        res = { "success": False, "message": "failed to mkdir" }
        return json.dumps(res)

    res = { "success": True, "message": "successfully created new directories" }
    return json.dumps(res)

@app.route("/upload", methods=['POST'])
@requires_auth
def upload():
    try:
        token = request.form['token']
        decoded = jwt.decode(token, server_config.JWT_SECRET, server_config.JWT_ALGORITHM )
        user_dir = "storage/" + decoded['username'] + "/"
        cur_dir = user_dir + request.form['cur_dir']
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(cur_dir, filename))
    except Exception:
        print "Unexpected error:", sys.exc_info()[0]
        res = { "success": False, "message": "failed to upload file" }
        return json.dumps(res)

    res = { "success": True, "message": "successfully uploaded file!" }
    return json.dumps(res)


server = wsgi.WSGIServer((server_config.SERVER_IP, server_config.SERVER_PORT), app)
server.serve_forever()
