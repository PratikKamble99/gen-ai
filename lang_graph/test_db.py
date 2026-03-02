from pymongo import MongoClient

client = MongoClient(
    "mongodb://root:password_123@localhost:27017/?authSource=admin"
)

print(client.admin.command("ping"))