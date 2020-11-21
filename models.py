import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .app import db


#############
#   USER    #
#############
class User(db.Model):
    __tablename__ = 'USER'

    _username = db.Column('u_username', db.String(255), primary_key=True)
    _password = db.Column('u_password', db.String(255), nullable=False)
    _date = db.Column('u_date', db.DateTime, nullable=False)

    _participations = relationship('Participation', back_populates='_user')

    def jsonify(self):
        return\
            {
                'username': self._username,
                'date': self._date.strftime("%Y-%m-%dT%H:%M:%S"),
            }


#############
#  DRAWING  #
#############
class Drawing(db.Model):
    __tablename__ = 'DRAWING'

    _id = db.Column('d_id', db.Integer, primary_key=True, autoincrement=True)
    _link = db.Column('d_link', db.String(255), nullable=False, unique=True)
    _date = db.Column('d_date', db.DateTime, nullable=False)

    _participation = relationship('Participation', back_populates='_drawing', uselist=False)

    def jsonify(self):
        return\
            {
                'id': self._id,
                'link': self._link,
                'date': self._date.strftime("%Y-%m-%dT%H:%M:%S"),
            }


#############
# CHALLENGE #
#############
class Challenge(db.Model):
    __tablename__ = 'CHALLENGE'

    _id = db.Column('c_id', db.Integer, primary_key=True, autoincrement=True)
    _name = db.Column('c_name', db.String(255), nullable=False)
    _type = db.Column('c_type', db.Boolean, nullable=False, default=False)
    _theme = db.Column('c_theme', db.String(255), nullable=False)
    _date = db.Column('c_duration', db.DateTime, nullable=False)
    _timer = db.Column('c_timer', db.Integer, nullable=False)

    _participations = relationship('Participation', back_populates='_challenge')

    def jsonify(self):
        return\
            {
                'id': self._id,
                'name': self._name,
                'type': self._type,
                'theme': self._theme,
                'date': self._date.strftime("%Y-%m-%dT%H:%M:%S"),
                'timer': self._timer,
            }


#############
# CHALLENGE #
#############
class Participation(db.Model):
    __tablename__ = 'PARTICIPATION'

    _user_id = db.Column('p_u_id', db.String(255), ForeignKey('USER.u_username', ondelete='CASCADE'), primary_key=True)
    _drawing_id = db.Column('p_d_id', db.Integer, ForeignKey('DRAWING.d_id', ondelete='CASCADE'), primary_key=True)
    _challenge_id = db.Column('p_c_id', db.Integer, ForeignKey('CHALLENGE.c_id', ondelete='CASCADE'), primary_key=True)

    _user = relationship('User', back_populates='_participations')
    _drawing = relationship('Drawing', back_populates='_participation')
    _challenge = relationship('Challenge', back_populates='_participations')
    _is_creator = db.Column('p_is_creator', db.Boolean, nullable=False)
    _votes = db.Column('p_votes', db.Integer, nullable=False, default=0)

    def jsonify(self):
        return\
            {
                'user': self._user_id,
                'drawing': self._drawing_id,
                'challenge': self._challenge_id,
                'is_creator': self._is_creator,
                'votes': self._votes,
            }
