from pymongo import MongoClient
import os
# uri = "mongodb+srv://asaxena7531:saxena7531@cluster0.gg2ei.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(os.getenv('MONGO_URL'))

db = client.rule_db
