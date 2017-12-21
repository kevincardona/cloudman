import json

def asignup(username, password):
    file = json.load(open('users.json'))
    for user in file["users"]:
        if (user['username'] == username):
            return "Username already exists"
    newuser = {
        'username': username,
        'password': password
    }
    file["users"].append(newuser)
    data = file
    with open('users.json', 'w') as outfile:
        json.dump(data, outfile)
    return "Signed up"


def alogin(username, password):
    file = json.load(open('users.json'))
    for user in file["users"]:
        if (user['username'] == username) & (user['password'] == password):
            return "Logged In"
    return "Failed to log in"

def authenticate():
    return "Authenticated"
