from sqlalchemy import ForeignKey, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import relationship
from .app import db


# Code used to enforce FOREIGNKEY for SQLite3
@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()

participation_user = db.Table('PARTICIPATION_TO_USER', db.Model.metadata,
        db.Column('u_id', db.String(255), ForeignKey('USER.u_username'), primary_key=True),
        db.Column('p_u_id', db.Integer, primary_key=True),
        db.Column('p_d_id', db.Integer, primary_key=True),
        db.Column('p_c_id', db.Integer, primary_key=True),
        db.ForeignKeyConstraint(
            ('p_u_id', 'p_d_id', 'p_c_id'),
            ('PARTICIPATION.p_u_id', 'PARTICIPATION.p_d_id', 'PARTICIPATION.p_c_id')
        ),
    )

#############
#   USER    #
#############
class User(db.Model):
    __tablename__ = 'USER'

    _username = db.Column('u_username', db.String(255), primary_key=True)
    _password = db.Column('u_password', db.String(255), nullable=False)
    _date = db.Column('u_date', db.DateTime, nullable=False)
    _salt = db.Column('u_salt', db.String(255), nullable=False)

    _participations = relationship('Participation', back_populates='_user', cascade='delete')

    _votes = relationship('Participation', secondary=participation_user, back_populates='_voters', cascade='delete')

    def jsonify(self):
        return\
            {
                'username': self._username,
                'date': self._date.strftime('%Y-%m-%dT%H:%M:%S'),
                'salt': self._salt,
            }


#############
#  DRAWING  #
#############
class Drawing(db.Model):
    __tablename__ = 'DRAWING'

    _id = db.Column('d_id', db.Integer, primary_key=True, autoincrement=True)
    _link = db.Column('d_link', db.String(255), nullable=False, unique=True)
    _date = db.Column('d_date', db.DateTime, nullable=False)

    _participation = relationship('Participation', back_populates='_drawing', cascade='delete', uselist=False)

    def jsonify(self):
        return\
            {
                'id': self._id,
                'link': self._link,
                'date': self._date.strftime('%Y-%m-%dT%H:%M:%S'),
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
    _desc = db.Column('c_desc', db.String(255), nullable=False)
    _date = db.Column('c_duration', db.DateTime, nullable=False)
    _timer = db.Column('c_timer', db.Integer, nullable=False)

    _participations = relationship('Participation', back_populates='_challenge', cascade='delete')

    def jsonify(self):
        return\
            {
                'id': self._id,
                'name': self._name,
                'type': self._type,
                'theme': self._theme,
                'desc' : self._desc,
                'date': self._date.strftime('%Y-%m-%dT%H:%M:%S'),
                'timer': self._timer,
            }


#################
# PARTICIPATION #
#################
class Participation(db.Model):
    __tablename__ = 'PARTICIPATION'

    _user_id = db.Column('p_u_id', db.String(255), ForeignKey('USER.u_username'), primary_key=True)
    _drawing_id = db.Column('p_d_id', db.Integer, ForeignKey('DRAWING.d_id'), primary_key=True)
    _challenge_id = db.Column('p_c_id', db.Integer, ForeignKey('CHALLENGE.c_id'), primary_key=True)

    _user = relationship('User', back_populates='_participations')
    _drawing = relationship('Drawing', back_populates='_participation')
    _challenge = relationship('Challenge', back_populates='_participations')
    _is_creator = db.Column('p_is_creator', db.Boolean, nullable=False)
    _votes = db.Column('p_votes', db.Integer, nullable=False, default=0)

    _voters = db.relationship('User', secondary=participation_user, back_populates='_votes', cascade='delete') 

    def jsonify(self):
        return\
            {
                'user': self._user_id,
                'drawing': self._drawing_id,
                'challenge': self._challenge_id,
                'is_creator': self._is_creator,
                'votes': self._votes,
            }