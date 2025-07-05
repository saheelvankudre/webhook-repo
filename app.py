from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# ✅ MongoDB connection string
MONGO_URI = "mongodb+srv://webhook_user:WebhookPass123@cluster0.drmc8gg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)

# ✅ use the correct DB and collection names
db = client['webhook_db']
collection = db['webhook_events']

@app.route('/')
def home():
    return render_template('index.html')  # Make sure templates/index.html exists

@app.route('/webhook', methods=['POST'])
def api_gh_message():
    if request.headers.get('Content-Type') == 'application/json':
        my_info = request.json
        print(f"Received JSON payload: {my_info}")

        # Save to MongoDB
        doc = {
            'request_id': my_info['request_id'],
            'author': my_info['author'],
            'action': my_info['action'],
            'from_branch': my_info['from_branch'],
            'to_branch': my_info['to_branch'],
            'timestamp': my_info['timestamp'],
        }
        result = collection.insert_one(doc)

        # Prepare response with _id as string
        doc['_id'] = str(result.inserted_id)

        return jsonify({"status": "success", "data": doc}), 200
    else:
        return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 400


@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort('_id', -1).limit(10))
    for event in events:
        event['_id'] = str(event['_id'])
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)
