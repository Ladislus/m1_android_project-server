from .app import app
from .models import *
from flask import jsonify

@app.route('/')
def hello_world():
    return 'Bonjour de flask!'

@app.route("/api/GetUser/<int:cleapi>")
def getUsers(cleapi):
    if cleapi == 123456:
        users = [utilisateur.jsonify() for utilisateur in Utilisateur.query.all()]
        return jsonify(users)
    else:
        return "Wrong key"

@app.route("/api/GetDessins/<int:cleapi>")
def getDessins(cleapi):
    if cleapi == 123456:
        dessins = [dessin.jsonify() for dessin in Dessin.query.all()]
        return jsonify(dessins)
    else:
        return "Wrong key"

@app.route("/api/GetChallenges/<int:cleapi>")
def getChalls(cleapi):
    if cleapi == 123456:
        challs = [chall.jsonify() for chall in Challenge.query.all()]
        return jsonify(challs)
    else:
        return "Wrong key"

@app.route("/api/GetChallenge/<int:idChall>/<int:cleapi>")
def getChall(idChall,cleapi):
    if cleapi == 123456:
        chall =  Challenge.query.get(idChall)
        return chall.jsonify()
    else:
        return "Wrong key"

@app.route("/api/GetParticipations/<pseudoUser>/<int:cleapi>")
def getParticipation(pseudoUser, cleapi):
    if cleapi == 123456:
        participations = [participation.jsonify() for participation in Utilisateur.query.get(str(pseudoUser)).getParticipation()]
        return jsonify(participations)
    else:
        return "Wrong key"

@app.route("/api/GetDessinsUser/<pseudoUser>/<int:cleapi>")
def getDessinsUser(pseudoUser, cleapi):
    if cleapi == 123456:
        dessins = [dessin.jsonify() for dessin in Utilisateur.query.get(str(pseudoUser)).getDessins()]
        return jsonify(dessins)

    else:
        return "Wrong key"

@app.route("/api/getDessinsChallenge/<int:idChall>/<int:cleapi>")
def getDessinsChallenge(idChall, cleapi):
    if cleapi == 123456:
        dessins = [dessin.jsonify() for dessin in Challenge.query.get(idChall).getDessins()]
        return jsonify(dessins)

    else:
        return "Wrong key"

@app.route("/api/getUsersChallenge/<int:idChall>/<int:cleapi>")
def getUsersChallenge(idChall, cleapi):
    if cleapi == 123456:
        users = [user.jsonify() for user in Challenge.query.get(idChall).getParticipants()]
        return jsonify(users)

    else:
        return "Wrong key"