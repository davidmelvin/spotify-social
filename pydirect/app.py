# from models import Result
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///concert_buddies'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String())
    name = db.Column(db.String())
    type = db.Column(db.String())

    def __init__(self, uri, name, type):
        self.url = uri
        self.name = name
        self.type = type

    def __repr__(self):
        return '<id {}>'.format(self.id)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()
