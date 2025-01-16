from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from bson import ObjectId 
from flask import current_app, g
from pymongo import MongoClient

mongo = PyMongo()
load_dotenv()

def get_db():
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
    iterinaries_collection = db['itinerary']
    search_hist_collection = db['search_history']

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return User(user)  
        return None
    
    from .views import views
    from .auth import auth
    auth.users_collection = users_collection
    views.iterinaries_collection = iterinaries_collection
    views.search_hist_collection = search_hist_collection

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app
