from pymongo import MongoClient
from bson import ObjectId
from typing import Literal
import datetime
import os
from dotenv import load_dotenv


load_dotenv()


class DatabaseManager:
    def __init__(
        self,
        location: Literal['remote', 'local'] = 'remote'): 
        
        if location == 'local':
            connection_string="mongodb://localhost:27017/"
        else:
            connection_string = os.getenv('DB_URI')
    
        self.client = MongoClient(connection_string)

        try:
            self.db = self.client.get_database('llm-summarizer')
        except Exception as e:
            raise Exception('Unable to find the database due to ', e)
        self.users_collection = self.db["users"]
        self.users_history = self.db["users_history"]

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

    def get_all_history(self):
        history = self.users_history.find()
        return [(str(item["_id"]), item["name"]) for item in history]

    def add_summarization_history(self, user_id, text, summary, name):
        history_id = self.users_history.insert_one({
            "user_id": user_id,
            "name": name,
            "date": datetime.datetime.now(),
            "text": text,
            "summary": summary
        })
        return str(history_id.inserted_id)

    def get_user_history(self, user_id):
        history = self.users_history.find({"user_id": user_id})
        result = [(str(item["_id"]), item["name"]) for item in history]
        print(result)
        return result

    def get_document_by_id(self, document_id):
        object_id = ObjectId(document_id)
        document = self.users_history.find_one({"_id": object_id})
        return document if document else None

    def delete_document_by_id(self, document_id):
        object_id = ObjectId(document_id)
        self.users_history.delete_one({"_id": object_id})

    def search_content(self, string, user_id):
        result = self.users_history.find({
            "$and": [
                {"text": {"$regex": string, "$options": "i"}},  # Case-insensitive regex search
                {"user_id": user_id}
            ]
        })
        return [(str(item["_id"]), item["name"]) for item in result]
    
    def search_summary(self, string, user_id):
        result = self.users_history.find({
            "$and": [
                {"summary": {"$regex": string, "$options": "i"}},  # Case-insensitive regex search
                {"user_id": user_id}
            ]
        })
        return [(str(item["_id"]), item["name"]) for item in result]
    
    def delete_user(self, user_id):
        object_id = ObjectId(user_id)
        self.users_collection.delete_one({"_id": object_id})
        self.users_history.delete_many({"user_id": user_id})