from .app import app
from .models import *
from flask import jsonify


@app.route("/api/GetAllUser")
def getAllUsers():
    users = [user.jsonify() for user in User.query.all()]
    return jsonify(users)
