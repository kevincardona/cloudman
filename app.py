from gevent import monkey
monkey.patch_all()
import jwt, json, requests, glob, os, server_config, sys
sys.path.append('routes/')
from flask import Flask, request, send_file, Response
from gevent import wsgi
from werkzeug.utils import secure_filename
from functools import wraps
from auth import asignup, alogin, authenticate
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# END OF IMPORTS + GLOBALS


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        print token
        if (authenticate(token) == False):
            res = { 'success': False, 'message': 'Invalid token' }
            return json.dumps(res)
        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=['GET', 'POST'])
def index ():
    res = json.dumps({'a':'b'})
    return Response(res, status=200, mimetype='application/json')

# TODO: Limit username/password character use + create user storage folder
@app.route("/signup", methods=['POST'])
def signup():
    req = request.get_json()
    username = req['username']
    password = req['password']
    return asignup(username, password)


@app.route("/login", methods=['POST'])
def login():
    try:
        raw = request.get_data()
        print raw
        req = request.get_json()
        return alogin(req['username'], req['password'])
    except Exception:
        try:
            print "FORM DATA BOI"
            print request.form['username']
            return alogin(request.form['username'], request.form['password'])
        except Exception:
            print "FAIL BOI"
            res = json.dumps({'success': False, 'message': 'Error!'})
            return Response(res, status=200, mimetype='application/json')
    res = json.dumps({'success': False, 'message': 'Bad request error!'})
    return Response(res, status=200, mimetype='application/json')


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
        res = { 'success': False, 'message': 'failed to send file' }
        return json.dumps(res)


#  TODO: clarify cur_dirs filtering capabilities
@app.route("/ls", methods=['POST'])
@requires_auth
def ls():
    try:
        token = request.headers.get('token')
        decoded = jwt.decode(token, server_config.JWT_SECRET, server_config.JWT_ALGORITHM )
        user_dir = "storage/" + decoded['username'] + "/"
        current_dir = user_dir + request.form['cur_dir'] + "*"
    except Exception:
        print "Unexpected error:", sys.exc_info()[0]
        res = { "success": False, "message": "failed to ls" }
        return json.dumps(res)
    files = []
    directories = []
    dir =  glob.glob(current_dir)
    count = 0
    while count < len(dir):
        print dir
        if os.path.isdir(dir[count]) :
            directories.append(dir[count])
        else:
            files.append(dir[count])
        count += 1
    res = { "success": True , "files": files, "directories": directories }
    return json.dumps(res)


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
        res = { "success": False, "message": "failed to upload file" }
        return json.dumps(res)

    res = { "success": True, "message": "successfully uploaded file!" }
    return json.dumps(res)


server = wsgi.WSGIServer((server_config.SERVER_IP, server_config.SERVER_PORT), app)
server.serve_forever()
