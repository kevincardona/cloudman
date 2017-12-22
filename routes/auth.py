import jwt
import json
import bcrypt
import server_config
from datetime import datetime, timedelta


def asignup(username, password):
    file = json.load(open('users.json'))
    for user in file["users"]:
        if (user['username'] == username):
            res = { "success": False, "message": "Username already exists!" }
            return json.dumps(res)
    hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    newuser = {
        'username': username,
        'password': hash
    }
    file["users"].append(newuser)
    data = file
    with open('users.json', 'w') as outfile:
        json.dump(data, outfile)
    res = { "success": True, "message": "Successfully signed up!" }
    return json.dumps(res)


def alogin(username, password):
    file = json.load(open('users.json'))
    for user in file["users"]:
        if (user['username'] == username):
            upass = user['password']
            if (bcrypt.hashpw(password.encode('utf-8'), upass.encode('utf-8'))) == user['password']:
                token_items = {
                    'username': user['username'],
                    'exp': datetime.utcnow() + timedelta(seconds=server_config.JWT_EXP_SECONDS)
                }
                token = jwt.encode(token_items, server_config.JWT_SECRET, server_config.JWT_ALGORITHM)
                res = { "success": True, "message": "Successfully logged in!", "token": token }
                return json.dumps(res)
    res = { "success": False, "message": "Invalid login information" }
    return json.dumps(res)

def authenticate(token):
    try:
        decoded = jwt.decode(token, server_config.JWT_SECRET, server_config.JWT_ALGORITHM )
        if (decoded):
            return True
        return False
    except Exception:
        return False
