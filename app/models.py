## for database models
from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(150))
    posts = db.relationship('Post')
    
class Post(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    date_posted = db.Column(db.DateTime(timezone=True), primary_key=True, default=func.now()) #retrieves current time and stores it in the DateTime field
    content = db.Column(db.String(10000))




