from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Db
Db = SQLAlchemy()


class Users(Db.Model):

    # Ref. to table
    __tablename__ = 'users'

    # Class fields match columns
    uid = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
    username = Db.Column(Db.String(64), nullable=False)
    first_name = Db.Column(Db.String(64), nullable=False)
    last_name = Db.Column(Db.String(64), nullable=False)
    password = Db.Column(Db.String(20), nullable=False)
    email = Db.Column(Db.String(64), nullable=False)