from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
# from api import db, users
#
# found = users.query.filter_by(name="Luis").first()
# if found:
#     print(found.name)
# else:
#     print("nom")
#session["user"] = "Jomb"
# user = "Luims"
# usr = users(user, "qwe@dfgfdghfghgf")
# db.session.add(usr)
# db.session.commit()

from datetime import date, datetime, timedelta
from faker import Faker
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    date_posted = db.Column(db.Date)
    datetime_posted = db.Column(db.DateTime)

@app.route('/')
def index():
    week = 0
    # dow = date.today().strftime("%w")
    # first_date = date.today() - timedelta(weeks=week)
    # first_date = first_date - timedelta(days=int(dow))
    # last_date = first_date - timedelta(weeks=1)
    #print(first_date)
    #print(first_date.strftime("%w"))


    first_date = date(2020, 5, 28)
    dow = first_date.strftime("%w")
    max = [0, 0, 0, 0, 0, 0, 0]
    d = int(dow)
    print(first_date)
    print(first_date.strftime("%w"))
    transactions = Transactions.query.filter_by(date_posted=first_date).all()
    for day in range(int(dow)):
        transactionsb = db.session.query(func.max(Transactions.amount)).filter_by(date_posted=first_date).first()
        max[d] = transactionsb[0]
        d -= 1
        first_date = first_date - timedelta(days=1)

    transactionsb = db.session.query(func.max(Transactions.amount)).filter_by(date_posted=first_date).first()
    max[d] = transactionsb[0]
    last_date = first_date - timedelta(weeks=1)

    transactions = Transactions.query.filter(Transactions.date_posted.between(last_date, first_date)).all()
    transactionsb = db.session.query(func.max(Transactions.amount)).filter \
        (Transactions.date_posted.between(last_date, first_date)).first()

    print(transactionsb[0])
    print(max)


    # for i in transactionsb:
    #     print(i[0])

    # for i in transactions:
    #     print(i.date_posted.strftime("%w"))
    # print(len(transactions))

    #transactions = Transactions.query.all()

    # transaction_date = date(2020, 5, 25)
    # transactions = Transactions.query.filter_by(date_posted=transaction_date).all()

    # transaction_date = date(2021, 8, 25)
    # transactions = Transactions.query.filter(func.strftime('%w', Transactions.date_posted) == "1").all()

    # transaction_date = date(2021, 8, 25)
    # transactions = Transactions.query.filter(func.date(Transactions.datetime_posted) == transaction_date).all(

    # first_date = date(2019, 6, 13)
    # last_date = date(2019, 6, 16)

    # transactions = Transactions.query.filter(Transactions.date_posted.between(first_date, last_date)).all()
    # for i in transactions:
    #     print(i.date_posted.strftime("%w"))
    # print(len(transactions))

    # first_date = date(2019, 6, 13)
    # last_date = date(2019, 6, 16)
    # transactions = Transactions.query.filter(Transactions.datetime_posted.between(first_date, last_date)).all()

    # transactions = Transactions.query.filter(Transactions.date_posted > date.today() - timedelta(weeks=1)).all()

    # transactions = Transactions.query.filter(Transactions.datetime_posted > datetime.now() - timedelta(days=30)).all()

    #transactions = db.session.query(Transactions.date_posted, func.sum(Transactions.amount)).group_by(Transactions.date_posted).all()
    # first_date = date(2019, 6, 13)
    # last_date = date(2019, 6, 16)
    # transactions = db.session.query(func.strftime('%w', Transactions.date_posted), Transactions.amount).\
    #     filter(Transactions.date_posted.between(first_date, last_date)).all()
    #
    # for i in transactions:
    #     print(i[0], i[1])
    #
    # print(len(transactions))



    # transactions = db.session.query(func.strftime('%Y', Transactions.date_posted), func.sum(Transactions.amount)).group_by(func.strftime('%Y', Transactions.date_posted)).all()

    #transactions = db.session.query(func.strftime('%Y-%m', Transactions.date_posted), func.sum(Transactions.amount)).group_by(func.strftime('%Y-%m', Transactions.date_posted)).all()

    return render_template('index.html', transactions=transactions)

if __name__ == "__main__":
    #db.create_all()
    app.run(threaded=True)


'''
db.create_all()
fake = Faker()
for _ in range(10000):
    transaction_date = fake.date_time_between(start_date='-3y')
    db.session.add(
        Transactions(
            amount=fake.random_int(),
            date_posted=transaction_date.date(),
            datetime_posted=transaction_date
        )
    )
db.session.commit()
'''
