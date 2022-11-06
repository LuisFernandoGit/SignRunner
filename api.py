from flask import Flask, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from passlib.hash import bcrypt
from datetime import date, timedelta
#from waitress import serve
import time

#Conecting flask application with database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Scores.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Tables definition
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    scoresN = db.relationship('Score', backref='player')
    scoresE = db.relationship('ScoreE', backref='player')
    scoresH = db.relationship('ScoreH', backref='player')

    def __init__(self, name, password):
        self.name = name
        self.password = bcrypt.encrypt(password)

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    score_date = db.Column(db.Date)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

    def __init__(self, score, score_date, player):
        self.score = score
        self.score_date = score_date
        self.player = player

class ScoreE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    score_date = db.Column(db.Date)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

    def __init__(self, score, score_date, player):
        self.score = score
        self.score_date = score_date
        self.player = player

class ScoreH(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    score_date = db.Column(db.Date)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

    def __init__(self, score, score_date, player):
        self.score = score
        self.score_date = score_date
        self.player = player

#Services and routes
@app.route('/signin', methods=['post'])
def signin():
    name = request.json['name']
    password = request.json['password']
    found = Player.query.filter_by(name=name).first()
    if found:
        return jsonify({"Response": "-1"})
    else:
        ply = Player(name, password)
        db.session.add(ply)
        db.session.commit()
        return jsonify({"Response": "1"})

@app.route('/login', methods=['post'])
def login():
    name = request.json['name']
    password = request.json['password']
    found = Player.query.filter_by(name=name).first()
    if found:
        if found.validate_password(password):
            return jsonify({"Response": str(found.id)})
        else:
            return jsonify({"Response": "-1"})
    else:
        return jsonify({"Response": "-1"})

@app.route('/historial/<difficulty>/<id>', methods=['post'])
def historial(difficulty, id):
    found = Player.query.filter_by(id=id).first()
    if found:
        day = request.json['day']
        month = request.json['month']
        year = request.json['year']

        first_date = date(int(year), int(month), int(day))
        dow = first_date.strftime("%w")
        dow = 6 - int(dow)
        first_date = first_date + timedelta(days=dow)
        max = [0, 0, 0, 0, 0, 0, 0]
        d = 6
        #print(first_date)
        #print(first_date.strftime("%w"))

        if difficulty == "n":
            points = Score.score
            dateP = Score.score_date
            playerid = Score.player_id
        elif difficulty == "e":
            points = ScoreE.score
            dateP = ScoreE.score_date
            playerid = ScoreE.player_id
        elif difficulty == "h":
            points = ScoreH.score
            dateP = ScoreH.score_date
            playerid = ScoreH.player_id

        for day in range(6):
            current_week = db.session.query(func.max(points)).filter_by(score_date=first_date,
                                                                             player_id=found.id).first()
            if current_week[0]:
                max[d] = current_week[0]
            d -= 1
            first_date = first_date - timedelta(days=1)
            # print(d)

        current_week = db.session.query(func.max(points)).filter_by(score_date=first_date,
                                                                         player_id=found.id).first()
        if current_week[0]:
            max[d] = current_week[0]
        last_date = first_date - timedelta(weeks=1)

        prev_week = db.session.query(func.max(points)).filter \
            (dateP.between(last_date, first_date), playerid == found.id).first()

        #print(prev_week)
        #print(max)

        if prev_week[0]:
            return jsonify({'week': max, 'prev_week': prev_week[0]})
        else:
            prev_week = [0, 0, 0, 0, 0, 0, 0]
            return jsonify({'week': max, 'prev_week': prev_week[0]})
    else:
        return jsonify({"week": "-1"})

@app.route('/promedio/<difficulty>/<id>', methods=['get'])
def promedio(difficulty, id):
    found = Player.query.filter_by(id=id).first()
    if found:
        #difficulty = request.json['difficulty']
        #difficulty = "n"
        if difficulty == "n":
            points = found.scoresN
        elif difficulty == "e":
            points = found.scoresE
        elif difficulty == "h":
            points = found.scoresH
        # for i in found.scores:
        #     print(i.score, i.score_date)
        if len(points) > 0:
            last = len(points) - 1
        else:
            return jsonify({"last": 0, "last_ten": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

        if len(points) > 10:
            prom = last - 10
            cont = 10
        else:
            prom = len(points) - last - 1
            cont = len(points) - 1

        last_ten = []
        last = points[last].score
        # print(last)

        for i in range(cont):
            # print(found.scores[prom].score)
            last_ten.append(points[prom].score)
            prom += 1

        return jsonify({"last": last, "last_ten": last_ten})

    else:
        return jsonify({"last": "-1"})

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5050, debug=False, threaded=True)
