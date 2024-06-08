from flask import Flask, request
from flask_cors import CORS
from os import path, remove
import threading
import json

from modules.logger import Logger
from modules.scrap import Scrap

# Configure application
app = Flask(__name__)
cors = CORS(app, resources={
            r"/api": {"origins": "*"}})

"""
Add user: {
    "action": "add-user",
    "data": "Username/URL
}

Delete user: {
    "action": "delete-user",
    "data": "Username/URL"
}

Get users: {
    "action": "list-users"
}

Set time: {
    "action": "set-time",
    "data": 10
}

"""

@app.route("/api", methods=["POST"])
def index():
    # Add user
    if request.form.get("action") == "add-user":
        users = json.load(open("./files/users.json"))
        user = request.form.get("data").split("/")[-1]

        if user not in users:
            users.append(user)

            json.dump(users, open("./files/users.json", "w"))

            return {"status": 200, "Message": "Successfully added user"}
        else:
            return {"status": 406, "Message": "User already exist"}

    # Delete user
    if request.form.get("action") == "delete-user":
        users = json.load(open("./files/users.json"))
        user = request.form.get("data").split("/")[-1]

        if user in users:
            if path.isfile(f"./files/users/{user}.txt"):
                remove(f"./files/users/{user}.txt")
            users.remove(user)

            json.dump(users, open("./files/users.json", "w"))
            return {"status": 200, "Message": "Successfully deleted user"}
        else:
            return {"status": 404, "Message": "User not found"}

    # Get list of users
    if request.form.get("action") == "list-users":
        users = json.load(open("./files/users.json"))

        return {"status": 200, "users": users}

    # Set Sleep duration
    if request.form.get("action") == "set-time":
        conf = json.load(open("./files/conf.json"))
        conf["sleep"] = int(request.form.get("data"))
        json.dump(conf, open("./files/conf.json", "w"))

        return {"status": 200, "Message": "Successfully set time"}

    return {"status": 403, "Message": "Bad request"}

if __name__ == "__main__":
    log = Logger()
    scrap = Scrap(log)

    thread = threading.Thread(target=scrap.run)
    thread.start()

    try:
        app.run()
    except KeyboardInterrupt:
        thread.join()
