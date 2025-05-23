# application/models.py
from . import db
from datetime import datetime
from flask_login import UserMixin
from passlib.hash import sha256_crypt


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=True)
    last_name = db.Column(db.String(255), unique=False, nullable=True)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_paid = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    authenticated = db.Column(db.Boolean, default=False)
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    # the code given by other user to join the app
    invited_code = db.Column(db.String(255))
    # the code generated to refer other potential users
    referral_code = db.Column(db.String(255), unique=True, nullable=False)

    def encode_api_key(self):
        self.api_key = sha256_crypt.hash(self.username + str(datetime.utcnow))

    def encode_password(self):
        self.password = sha256_crypt.hash(self.password)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def to_json(self):
        # return {
        #     'first_name': self.first_name,
        #     'last_name': self.last_name,
        #     'username': self.username,
        #     'email': self.email,
        #     'id': self.id,
        #     'api_key': self.api_key,
        #     'is_active': True,
        #     'is_paid': self.is_paid
        # }

        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'id': self.id,
            'is_active': True,
            'is_paid': self.is_paid
        }


       