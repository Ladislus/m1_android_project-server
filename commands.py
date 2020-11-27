from .app import *
from .models import *
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

    u = User(_username='MamanGvomi', _password='$2a$12$8RIcKP1eNY6N48K0Apqc/ezEranNfK0jhvM5b0AqVPipyzuwDL4uW', _date=datetime.datetime.now(), _salt='$2a$12$8RIcKP1eNY6N48K0Apqc/e')
    u0 = User(_username='LHommeElastic', _password='$2a$12$kboUKvhiGgMU1q4r/kcUbuGCd8H9Mfu3rpDbolScpbL./ZrINL9B2', _date=datetime.datetime.now(), _salt='$2a$12$kboUKvhiGgMU1q4r/kcUbu')
    u1 = User(_username='WeeboMaster', _password='$2a$12$Z4LCvcPIRI/hofjy8k6oaO.BVS0x/N7qIhgG.Xrmfgd21Kb/EaVQi', _date=datetime.datetime.now(), _salt='$2a$12$Z4LCvcPIRI/hofjy8k6oaO')
    db.session.add_all([u, u0, u1])
    db.session.commit()

    c = Challenge(
        _name='Chien mignon',
        _type=True,
        _theme='https://www.notretemps.com/cache/com_zoo_images/c9/nom-chiot_d7378d62ea795a70b121a517c938b895.jpg',
        _desc="Bonjour les amies ! Il s'agit de dessiner ce poti chiot tous mignon ! Bonne chance !!!",
        _date=datetime.date(2020, 11, 5),
        _timer=30
    )
    db.session.add(c)
    db.session.commit()

    d = Drawing(_link='https://proactivecreative.com/wp-content/uploads/2019/10/how-to-draw-a-dog--768x555.jpg', _date=datetime.datetime.now())
    d0 = Drawing(_link='https://i.pinimg.com/564x/0f/d9/98/0fd998799eceba85f138964def66085d.jpg', _date=datetime.datetime.now())
    db.session.add_all([d, d0])
    db.session.commit()

    db.session.add_all(
        [
            Participation(
                _challenge_id=c._id,
                _user_id=u._username,
                _drawing_id=d._id,
                _is_creator=True,
                _votes=0),
            Participation(
                _challenge_id=c._id,
                _user_id=u0._username,
                _drawing_id=d0._id,
                _is_creator=True,
                _votes=0)
        ]
    )
    db.session.commit()
