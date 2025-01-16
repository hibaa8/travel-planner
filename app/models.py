from flask import current_app
from flask_login import UserMixin
from sqlalchemy.sql import func
from bson import ObjectId 
from werkzeug.local import LocalProxy


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.email = user_data["email"]
        self.password_hash = user_data["password"]

    def get(user_id, users_collection):
        """
        Fetch a user from the database by ID.
        """
        user_data = users_collection.find_one({"_id": ObjectId(user_id)})
        return User(user_data) if user_data else None
