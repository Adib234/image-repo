from pymongo import MongoClient
import os
import datetime


connection = os.environ.get(
    'MONGO_URI', '/Users/admin/shopifysummer2021/backend')


client = MongoClient(connection)


user = {"email": "Mike",  "password_hash": "My first blog post!", "images_private": [
    "mongodb", "python", "pymongo"], "bucket_name": "bucket1", "signed_up": datetime.datetime.utcnow()}

db = client["shopify-mongo"]
print(db)
users = db["users"]
print(db.list_collection_names())
users.insert_one(user).inserted_id
