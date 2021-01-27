from passlib.apps import custom_app_context as pwd_context
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)


class User(db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    images_private = db.Column(db.Text, nullable=True)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
