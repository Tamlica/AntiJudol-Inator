import uuid

from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'streamer'
    streaming_links = db.Column(db.JSON, nullable=True)  # Only for streamer, optional
    clean_option = db.Column(db.String(10), nullable=True)  # 'random' or 'fixed'
    fixed_supporter = db.Column(db.String(256), nullable=True, default="Kind Supporter")
    fixed_message = db.Column(db.String(256), nullable=True, default="Thank you for your support!")
    
    bad_words = db.relationship('BadWord', backref='user', lazy=True, cascade="all, delete-orphan")
    good_words = db.relationship('GoodWord', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class BadWord(db.Model):
    __tablename__ = 'bad_words'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

class GoodWord(db.Model):
    __tablename__ = 'good_words'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
