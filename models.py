from .app import db
from sqlalchemy.types import DateTime
import datetime

#participant_challenge = db.Table('participant_challenge', db.Model.metadata,
                        #     db.Column('id_challenge', db.Integer, db.ForeignKey('challenge.id'), primary_key=True),
                        #     db.Column('pseudo_utilisateur', db.String(255), db.ForeignKey('utilisateur.pseudo'), primary_key=True),
                        #     db.Column('id_img', db.Integer, db.ForeignKey('dessin.id')),
                        #     db.Column('is_creator', db.Boolean),
                        #     db.Column('nb_vote', db.Integer)
                        # )

class Participant_Challenge(db.Model):
    __tablename__ = 'participant_challenge'
    id_challenge = db.Column(db.Integer, db.ForeignKey('challenge.id'), primary_key=True)
    pseudo_utilisateur = db.Column(db.String(255), db.ForeignKey('utilisateur.pseudo'), primary_key=True)
    id_img = db.Column(db.Integer, db.ForeignKey('dessin.id'))
    is_creator = db.Column(db.Boolean)
    nb_vote = db.Column(db.Integer)


    def jsonify(self):
        participation = {
            'id_challenge': self.id_challenge,
            'pseudo_utilisateur': self.pseudo_utilisateur,
            'id_img': self.id_img,
            'is_creator' : self.is_creator,
            'nb_vote' : self.nb_vote,
        }
        return participation


class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    pseudo = db.Column(db.String(255), primary_key=True)
    mdp = db.Column(db.String(255), nullable=False)
    date = db.Column(DateTime(), default=datetime.datetime.utcnow)

    def jsonify(self):
        user = {
            'pseudo': self.pseudo,
            'date': self.date,
            'mdp': self.mdp,
        }
        return user

    def getParticipation(self):
        return Participant_Challenge.query.filter_by(pseudo_utilisateur=self.pseudo).all()

    def getDessins(self):
        return Dessin.query.join(Participant_Challenge, Dessin.id == Participant_Challenge.id_img).filter(Participant_Challenge.pseudo_utilisateur == self.pseudo).all()


class Dessin(db.Model):
    __tablename__ = 'dessin'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    contenu = db.Column(db.String(255), nullable=False) #lien ?
    date = db.Column(DateTime(), default=datetime.datetime.utcnow)

    def jsonify(self):
        dessin = {
            'id': self.id,
            'lien': self.contenu,
            'date': self.date,
        }
        return dessin

class Challenge(db.Model):
    __tablename__ = 'challenge'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nomImgTheme = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Boolean)
    theme = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False) #Champs desc
    duree = db.Column(DateTime(), default=datetime.datetime.utcnow) #Datefin ?
    timer = db.Column(db.Integer)

    def getDessins(self):
        return Dessin.query.join(Participant_Challenge, Dessin.id == Participant_Challenge.id_img).filter(Participant_Challenge.id_challenge == self.id).all()

    def getParticipants(self):
        return Utilisateur.query.join(Participant_Challenge, Utilisateur.pseudo == Participant_Challenge.pseudo_utilisateur).filter(Participant_Challenge.id_challenge == self.id).all()

    def jsonify(self):
        challenge = {
            'id': self.id,
            'nomImgTheme': self.nomImgTheme,
            'type': self.type,
            'theme': self.theme,
            'description' : self.description,
            'duree': self.duree,
            'timer': self.timer,
        }
        return challenge


