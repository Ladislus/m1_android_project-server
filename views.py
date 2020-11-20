from flask import jsonify

from .app import app


@app.route("/api/GetAllUser")
def getAllUsers():
    users = [user.jsonify() for user in getAllUsers()]
    return jsonify(users)
