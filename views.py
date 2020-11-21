import operator
import datetime
from .app import *
from .models import *
from flask import jsonify, request, redirect, url_for
from sqlalchemy.exc import IntegrityError

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

#   ERROR REPONSES
def wrong_api_key():
    return {'error': 'Invalid api_key'}, 403


def missing_argument(arg):
    return {'error': 'Missing argument:' + arg}, 400


def insertion_error(error):
    return {'error': 'Unable to save', 'details': error}, 409


#   GOOD RESPONSES
def nothing_found():
    return {}, 204


def reply(resp):
    return jsonify(resp), 200


#   UTILITIES
def valid_key(req):
    return req.headers.get('apiKey') == os.getenv('API_KEY')


#       ##############
#       #   Routes   #
#       ##############

#   DEBUG
@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('debug'))


@app.route('/api/debug', methods=['GET'])
def debug():
    return reply(os.getenv('API_KEY'))


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


@app.route('/api/user/save', methods=['POST'])
def api_user_save():
    if not valid_key(request):
        return wrong_api_key()
    user = User(
        _username=request.json.get('username'),
        _password=request.json.get('password'),
        _date=datetime.datetime.strptime(request.json.get('date'), '%Y-%m-%dT%H:%M:%S')
    )
    try:
        db.session.add(user)
        db.session.commit()
        return reply(user.jsonify())
    except IntegrityError as e:
        return insertion_error(e._message())


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


@app.route('/api/drawing/save', methods=['POST'])
def api_drawing_save():
    if not valid_key(request):
        return wrong_api_key()
    drawing = Drawing(
        _link=request.json.get('link'),
        _date=datetime.datetime.strptime(request.json.get('date'), '%Y-%m-%dT%H:%M:%S')
    )
    try:
        db.session.add(drawing)
        db.session.commit()
        return reply(drawing.jsonify())
    except IntegrityError as e:
        return insertion_error(e._message())


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


@app.route('/api/challenge/save', methods=['POST'])
def api_challenge_save():
    if not valid_key(request):
        return wrong_api_key()
    challenge = Challenge(
        _name=request.json.get('name'),
        _type=request.json.get('type'),
        _theme=request.json.get('theme'),
        _date=datetime.datetime.strptime(request.json.get('date'), '%Y-%m-%dT%H:%M:%S'),
        _timer=request.json.get('timer')
    )
    try:
        db.session.add(challenge)
        db.session.commit()
        return reply(challenge.jsonify())
    except IntegrityError as e:
        return insertion_error(e._message())


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
    participations = q.all()
    if len(participations) == 0:
        return nothing_found()
    return reply([participation.jsonify() for participation in participations])


@app.route('/api/participation/save', methods=['POST'])
def api_participation_save():
    if not valid_key(request):
        return wrong_api_key()
    participation = Participation(
        _user_id=request.json.get('u_id'),
        _drawing_id=request.json.get('d_id'),
        _challenge_id=request.json.get('c_id'),
        _is_creator=request.json.get('is_creator'),
        _votes=request.json.get('votes')
    )
    try:
        db.session.add(participation)
        db.session.commit()
        return reply(participation.jsonify())
    except IntegrityError as e:
        return insertion_error(e._message())
