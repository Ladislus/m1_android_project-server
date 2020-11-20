import os

from .app import *
from .models import *
from flask import jsonify, request


#       #########################
#       #   Utility functions   #
#       #########################

#   BAD REQUESTS
def wrong_api_key():
    return {'error': 'Invalid api_key'}, 403


def missing_argument(arg):
    return {'error': 'Missing argument:' + arg}, 400


#   RESPONSES
def nothing_found():
    return {}, 204


def reply(resp):
    return jsonify(resp), 200


#   UTILITIES
def valid_request(req):
    return req.headers.get('api_key') == os.environ.get('API_KEY')


#       ##############
#       #   Routes   #
#       ##############

#   FULL
@app.route('/api/full', methods=['GET'])
def api_full():
    if not valid_request(request):
        return wrong_api_key()
    return reply(
        {
            'users': [user.jsonify() for user in User.query.all()],
            'drawings': [drawing.jsonify() for drawing in Drawing.query.all()],
            'challenges': [challenge.jsonify() for challenge in Challenge.query.all()],
            'participations': [participation.jsonify() for participation in Participation.query.all()]
        }
    )


#   USERS
@app.route('/api/user/getall', methods=['GET'])
def api_user_getall():
    return reply([user.jsonify() for user in User.query.all()])


@app.route('/api/user/get', methods=['GET'])
def api_user_get():
    if not valid_request(request):
        return wrong_api_key()
    if 'username' not in request.args:
        return missing_argument('username')
    u = User.query.get(request.args.get('username'))
    if u is not None:
        return reply(u.jsonify())
    return nothing_found()


#   DRAWINGS
@app.route('/api/drawing/getall', methods=['GET'])
def api_drawing_getall():
    return reply([drawing.jsonify() for drawing in Drawing.query.all()])


@app.route('/api/drawing/get', methods=['GET'])
def api_drawing_get():
    if not valid_request(request):
        return wrong_api_key()
    if 'id' not in request.args:
        return missing_argument('id')
    d = Drawing.query.get(request.args.get('id'))
    if d is not None:
        return reply(d.jsonify())
    return nothing_found()


#   CHALLENGES
@app.route('/api/challenge/getall', methods=['GET'])
def api_challenge_getall():
    return jsonify([challenge.jsonify() for challenge in Challenge.query.all()]), 200


@app.route('/api/challenge/get', methods=['GET'])
def api_challenge_get():
    if not valid_request(request):
        return wrong_api_key()
    if 'id' not in request.args:
        return missing_argument('id')
    c = Challenge.query.get(request.args.get('id'))
    if c is not None:
        return reply(c.jsonify())
    return nothing_found()


#   PARTICIPATIONS
@app.route('/api/participation/getall', methods=['GET'])
def api_participation_getall():
    return jsonify([participation.jsonify() for participation in Participation.query.all()]), 200


@app.route('/api/participation/get', methods=['GET'])
def api_participation_get():
    if not valid_request(request):
        return wrong_api_key()
    if 'u_id' not in request.args:
        return missing_argument('u_id')
    if 'd_id' not in request.args:
        return missing_argument('d_id')
    if 'c_id' not in request.args:
        return missing_argument('c_id')
    c = Participation.query.get((request.args.get('u_id'), request.args.get('d_id'), request.args.get('c_id')))
    if c is not None:
        return reply(c.jsonify())
    return nothing_found()
