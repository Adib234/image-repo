from passlib.apps import custom_app_context as pwd_context
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    images_private = db.Column(db.Text, nullable=True)
    bucket_name = db.Column(db.String(20), nullable=True)
    signed_up = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "User({})".format(self.email)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
