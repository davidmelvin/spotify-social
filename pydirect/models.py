from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.String(), index=True, unique=True)
    name = db.Column(db.String())
    type = db.Column(ENUM('artist', 'user', name='account_type_enum'))

    def __init__(self, source_id, name, type):
        self.source_id = source_id
        self.name = name
        self.type = type

    def __repr__(self):
        return f'<id {self.id}/ source id: {self.source_id}: {self.type}: {self.name}>'.format(self.id)


class Follow(db.Model):
    __tablename__ = 'follower'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(
        db.String(), ForeignKey("account.source_id"), index=True)
    following_id = db.Column(
        db.String(), ForeignKey("account.source_id"), index=True)

    def __init__(self, follower_id, following_id):
        self.follower_id = follower_id
        self.following_id = following_id

    def __repr__(self):
        return f'<id {self.id}: {self.follower_id} following {self.following_id}>'
