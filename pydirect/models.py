from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String())
    name = db.Column(db.String())
    type = db.Column(db.String())

    def __init__(self, uri, name, type):
        self.uri = uri
        self.name = name
        self.type = type

    def __repr__(self):
        return '<id {}>'.format(self.id)
