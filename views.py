import os
import operator
from .app import *
from .models import *
from flask import jsonify, request

#       ##########################
#       #   Utility variables    #
#       ##########################

operators = {
    'eq': operator.eq,
    'lt': operator.lt,
    'le': operator.le,
    'gt': operator.gt,
    'ge': operator.ge,
    'ne': operator.ne,
}

columns = {
    'user': {
        'username': User._username,
        'password': User._password,
        'date': User._date
    },
    'drawing': {
        'id': Drawing._id,
        'link': Drawing._link,
        'date': Drawing._date
    },
    'challenge': {
        'id': Challenge._id,
        'name': Challenge._name,
        'type': Challenge._type,
        'date': Challenge._date,
        'timer': Challenge._timer
    },
    'participation': {
        'u_id': Participation._user_id,
        'd_id': Participation._drawing_id,
        'c_id': Participation._challenge_id,
        'is_creator': Participation._is_creator,
        'votes': Participation._votes
    }
}


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
def valid_key(req):
    return req.headers.get('api_key') == os.environ.get('API_KEY')


#       ##############
#       #   Routes   #
#       ##############

#   FULL
@app.route('/api/full', methods=['GET'])
def api_full():
    if not valid_key(request):
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
    if not valid_key(request):
        return wrong_api_key()
    users = User.query.all()
    if len(users) == 0:
        return nothing_found()
    return reply([user.jsonify() for user in users])


@app.route('/api/user/get', methods=['GET'])
def api_user_get():
    if not valid_key(request):
        return wrong_api_key()
    if 'username' not in request.args:
        return missing_argument('username')
    u = User.query.get(request.args.get('username'))
    if u is not None:
        return reply(u.jsonify())
    return nothing_found()


@app.route('/api/user/getwhere', methods=['POST'])
def api_user_getwhere():
    if not valid_key(request):
        return wrong_api_key()
    q = User.query
    for field, params in request.json.items():
        try:
            q = q.filter(operators[params['operator']](columns['user'][field], request.json[field]['value']))
        except KeyError:
            pass  # Ignore unknown fields or operators
    users = q.all()
    if len(users) == 0:
        return nothing_found()
    return reply([user.jsonify() for user in users])


#   DRAWINGS
@app.route('/api/drawing/getall', methods=['GET'])
def api_drawing_getall():
    if not valid_key(request):
        return wrong_api_key()
    drawings = Drawing.query.all()
    if len(drawings) == 0:
        return nothing_found()
    return reply([drawing.jsonify() for drawing in drawings])


@app.route('/api/drawing/get', methods=['GET'])
def api_drawing_get():
    if not valid_key(request):
        return wrong_api_key()
    if 'id' not in request.args:
        return missing_argument('id')
    d = Drawing.query.get(request.args.get('id'))
    if d is not None:
        return reply(d.jsonify())
    return nothing_found()


@app.route('/api/drawing/getwhere', methods=['POST'])
def api_drawing_getwhere():
    if not valid_key(request):
        return wrong_api_key()
    q = Drawing.query
    for field, params in request.json.items():
        try:
            q = q.filter(operators[params['operator']](columns['drawing'][field], request.json[field]['value']))
        except KeyError:
            pass  # Ignore unknown fields or operators
    drawings = q.all()
    if len(drawings) == 0:
        return nothing_found()
    return reply([drawing.jsonify() for drawing in drawings])


#   CHALLENGES
@app.route('/api/challenge/getall', methods=['GET'])
def api_challenge_getall():
    if not valid_key(request):
        return wrong_api_key()
    challenges = Challenge.query.all()
    if len(challenges) == 0:
        return nothing_found()
    return jsonify([challenge.jsonify() for challenge in challenges]), 200


@app.route('/api/challenge/get', methods=['GET'])
def api_challenge_get():
    if not valid_key(request):
        return wrong_api_key()
    if 'id' not in request.args:
        return missing_argument('id')
    c = Challenge.query.get(request.args.get('id'))
    if c is not None:
        return reply(c.jsonify())
    return nothing_found()


@app.route('/api/challenge/getwhere', methods=['POST'])
def api_challenge_getwhere():
    if not valid_key(request):
        return wrong_api_key()
    q = Challenge.query
    for field, params in request.json.items():
        try:
            q = q.filter(operators[params['operator']](columns['challenge'][field], request.json[field]['value']))
        except KeyError:
            pass  # Ignore unknown fields or operators
    challenges = q.all()
    if len(challenges) == 0:
        return nothing_found()
    return reply([challenge.jsonify() for challenge in challenges])


#   PARTICIPATIONS
@app.route('/api/participation/getall', methods=['GET'])
def api_participation_getall():
    if not valid_key(request):
        return wrong_api_key()
    participations = Participation.query.all()
    if len(participations) == 0:
        return nothing_found()
    return jsonify([participation.jsonify() for participation in participations]), 200


@app.route('/api/participation/get', methods=['GET'])
def api_participation_get():
    if not valid_key(request):
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


@app.route('/api/participation/getwhere', methods=['POST'])
def api_participation_getwhere():
    if not valid_key(request):
        return wrong_api_key()
    q = Participation.query
    for field, params in request.json.items():
        try:
            q = q.filter(operators[params['operator']](columns['participation'][field], request.json[field]['value']))
        except KeyError:
            pass
    print(q)
    participations = q.all()
    if len(participations) == 0:
        return nothing_found()
    return reply([participation.jsonify() for participation in participations])
