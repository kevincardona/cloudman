import json
import bcrypt
import server_config

def asignup(username, password):
    file = json.load(open('users.json'))
    for user in file["users"]:
        if (user['username'] == username):
            return "Username already exists"

    hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    newuser = {
        'username': username,
        'password': hash
    }
    file["users"].append(newuser)
    data = file
    with open('users.json', 'w') as outfile:
        json.dump(data, outfile)
    return "Signed up"


def alogin(username, password):
    file = json.load(open('users.json'))
    for user in file["users"]:
        if (user['username'] == username):
            upass = user['password']
            if (bcrypt.hashpw(password.encode('utf-8'), upass.encode('utf-8'))) == user['password']:
                return "Logged In"
    return "Failed to log in"

def authenticate():
    return "Authenticated"
