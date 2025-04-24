from app import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def login_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="fb96dc9d77bfdf8c.jpg")
    paswd = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def  get_reset_token(self):
        s=Serializer(current_app.config['SECRET_KEY'])
        token=s.dumps({'user_id' : self.id})
        # data = s.loads(token, max_age=expires_time)
        return token
    
    @staticmethod
    def verify_reset_token(token, expires_time=1800):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_time)['user_id']
        except:
            return None
        
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.user_name}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(50), nullable=False)
    date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text, nullable=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"

# Check if the database file exists
    

