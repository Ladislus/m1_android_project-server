from .app import app, db
from .models import Utilisateur, Dessin, Challenge, Participant_Challenge
import urllib.request, json
import datetime


@app.cli.command()
def resetdb():
    """Suppression et création des tables"""
    db.drop_all()
    db.create_all()

@app.cli.command()
def syncdb():
    """Création des tables manquantes"""
    db.create_all()

@app.cli.command()
def testmodel():
    """Peuplage test bd"""
    user = Utilisateur(pseudo="MamanGvomi", mdp="AbricotSex")
    user2 = Utilisateur(pseudo="LHommeElastic", mdp="JeSuisLadislas")
    user3 = Utilisateur(pseudo="WeeboMaster", mdp="Tom")
    db.session.add(user)
    db.session.commit()
    db.session.add(user2)
    db.session.commit()
    db.session.add(user3)
    db.session.commit()

    chall = Challenge(
        nomImgTheme="Chien mignon",
        type = True,
        theme = "https://www.notretemps.com/cache/com_zoo_images/c9/nom-chiot_d7378d62ea795a70b121a517c938b895.jpg",
        description = "Bonjour ! Vous allez devoir dessiner ce joli chien tout mignon en moins de 30 minutes !!! Que le meilleurs gagne :)",
        duree = datetime.date(2020, 11, 5),
        timer = 30 #30min ?
    )
    db.session.add(chall)
    db.session.commit()


    dessin = Dessin(
        contenu = "https://proactivecreative.com/wp-content/uploads/2019/10/how-to-draw-a-dog--768x555.jpg",
    )
    db.session.add(dessin)
    db.session.commit()

    dessin2 = Dessin(
        contenu = "https://i.pinimg.com/564x/0f/d9/98/0fd998799eceba85f138964def66085d.jpg",
    )
    db.session.add(dessin2)
    db.session.commit()

    participation = Participant_Challenge(
        id_challenge = chall.id,
        pseudo_utilisateur = user.pseudo,
        id_img = dessin.id,
        is_creator = True,
        nb_vote = 0
    )
    participation2 = Participant_Challenge(
        id_challenge = chall.id,
        pseudo_utilisateur = user2.pseudo,
        id_img = dessin2.id,
        is_creator = True,
        nb_vote = 0
    )

    db.session.add(participation)
    db.session.commit()
    db.session.add(participation2)
    db.session.commit()



