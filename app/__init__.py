from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from bson import ObjectId 
from .models import User
from flask import current_app, g
from werkzeug.local import LocalProxy
from pymongo import MongoClient

mongo = PyMongo()
load_dotenv()

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 
    app.config['MONGO_URI'] = os.getenv('MONGO_URI') 

    client = MongoClient(os.getenv('MONGO_URI') )
    db = client['travel-app']
    users_collection = db['user']

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Flask-Login user loader
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return User(user)  # Convert to a User object (see below)
        return None
    
    # Register blueprints
    from .views import views
    from .auth import auth
    auth.users_collection = users_collection

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app
