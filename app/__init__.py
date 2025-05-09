from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .config import Config   
    

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login_func"
login_manager.login_message_category = "info"




def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    login_manager.init_app(app=app)
    bcrypt.init_app(app=app)
    db.init_app(app=app)
    
    from app.users.routes import users
    from app.posts.routes import posts
    from app.main.routes import main
    from .errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app