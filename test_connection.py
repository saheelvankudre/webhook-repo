from pymongo import MongoClient

MONGO_URI = "mongodb+srv://webhook_user:WebhookPass123@cluster0.drmc8gg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URI)
    db = client["webhook_db"]
    print("✅ Connected successfully!")
    print("Collections:", db.list_collection_names())
except Exception as e:
    print("❌ Connection failed:", e)
