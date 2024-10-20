from pymongo import MongoClient
uri = "mongodb+srv://asaxena7531:saxena7531@cluster0.gg2ei.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

db = client.rule_db
