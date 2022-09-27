from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID


import uuid


db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = db.Column(db.String(), unique=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    type = db.Column(
        ENUM('artist', 'user', name='account_type_enum'), nullable=False)

    created_at = db.Column(
        TIMESTAMP, server_default=func.now(), nullable=False)
    created_by = db.Column(db.String(), nullable=False,
                           server_default="server")

    updated_at = db.Column(TIMESTAMP, server_default=func.now(),
                           onupdate=func.now(), nullable=False)
    updated_by = db.Column(db.String(), nullable=False,
                           server_default="server")

    def __init__(self, source_id, name, type):
        self.source_id = source_id
        self.name = name
        self.type = type

    def as_dict(self):
        return {
            "id": self.id if self.id else uuid.uuid4(),
            "source_id": self.source_id,
            "name": self.name,
            "type": self.type
        }

    def as_dict_without_id(self):
        d = self.as_dict()
        d.pop('id')
        return d

    def __repr__(self):
        return f'<id {self.id}/ source id: {self.source_id}: {self.type}: {self.name}>'.format(self.id)


account_source_id_index = Index('idx_account_source_id', Account.source_id)


if __name__ == '__main__':
    engine = db.get_engine()
    account_source_id_index.create(bind=engine)


class Follow(db.Model):
    __tablename__ = 'follower'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)

    # both of these are primary keys of the table, together
    follower_id = db.Column(
        db.String(), ForeignKey("account.source_id"), index=True, primary_key=True)
    following_id = db.Column(
        db.String(), ForeignKey("account.source_id"), index=True, primary_key=True)

    created_at = db.Column(
        TIMESTAMP, server_default=func.now(), nullable=False)
    created_by = db.Column(db.String(), nullable=False,
                           server_default="server")

    updated_at = db.Column(TIMESTAMP, server_default=func.now(),
                           onupdate=func.now(), nullable=False)
    updated_by = db.Column(db.String(), nullable=False,
                           server_default="server")

    def __init__(self, follower_id, following_id):
        self.follower_id = follower_id
        self.following_id = following_id

    def as_dict(self):
        return {
            "id": self.id if self.id else uuid.uuid4(),
            "follower_id": self.follower_id,
            "following_id": self.following_id
        }

    def as_dict_without_id(self):
        d = self.as_dict()
        d.pop('id')
        return d

    def __repr__(self):
        return f'<id {self.id}: {self.follower_id} following {self.following_id}>'
