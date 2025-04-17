from pymongo import MongoClient
from bson import ObjectId

class DatabaseManager:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        self.client = MongoClient(connection_string)
        self.db = self.client["user_management"]
        self.users_collection = self.db["users"]


    def add_user(self, username):
        result = self.users_collection.insert_one({
            "username": username
        })
        return result.inserted_id

    def user_exists(self, username):
        user = self.users_collection.find_one({"username": username})
        return user["_id"] if user else None
    
    def get_user_preferences(self, user_id):
        object_id = ObjectId(user_id)
        user = self.users_collection.find_one({"_id": object_id})
        if user and "preferences" in user:
            return user["preferences"]
        return []
    
    def save_user_preference(self, user_id, preferences):
        object_id = ObjectId(user_id)
        self.users_collection.update_one(
            {"_id": object_id},
            {"$set": {"preferences": preferences}}
        )
    
    def get_user(self, user_id):
        object_id = ObjectId(user_id)
        user = self.users_collection.find_one({"_id": object_id})
        return user if user else None