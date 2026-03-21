import os
import sqlite3
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "")

class StorageHandler:
    def __init__(self):
        self.use_sqlite = False
        try:
            if not MONGO_URI:
                raise ValueError("No MONGO_URI found in environment.")
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
            self.client.admin.command('ping') 
            self.db = self.client['ticket_classifier']
            self.collection = self.db['tickets']
            print("✅ Connected to MongoDB Atlas")
        except Exception as e:
            print(f"⚠️ MongoDB connection failed. Falling back to SQLite.")
            self.use_sqlite = True
            self._init_sqlite()

    def _init_sqlite(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect('data/local_tickets.db', check_same_thread=False)
        # UPDATED: Added draft_response column
        self.conn.execute('''CREATE TABLE IF NOT EXISTS tickets
                             (ticket_id TEXT PRIMARY KEY, ticket_text TEXT, category TEXT, 
                              urgency TEXT, confidence REAL, timestamp TEXT, draft_response TEXT)''')
        self.conn.commit()

    def save_ticket(self, data: dict):
        data['timestamp'] = datetime.now().isoformat()
        if self.use_sqlite:
            # UPDATED: Insert the draft response into SQLite
            self.conn.execute("INSERT INTO tickets VALUES (?,?,?,?,?,?,?)", 
                (data['ticket_id'], data['ticket_text'], data['category'], 
                 data['urgency'], data['confidence'], data['timestamp'], data.get('draft_response', '')))
            self.conn.commit()
        else:
            self.collection.insert_one(data)

    def get_recent_tickets(self, limit=50):
        if self.use_sqlite:
            cursor = self.conn.execute("SELECT * FROM tickets ORDER BY timestamp DESC LIMIT ?", (limit,))
            cols = [column[0] for column in cursor.description]
            return [dict(zip(cols, row)) for row in cursor.fetchall()]
        return list(self.collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(limit))
            
    def get_stats(self):
        tickets = self.get_recent_tickets(1000)
        categories = {}
        for t in tickets:
            cat = t.get('category', 'general')
            categories[cat] = categories.get(cat, 0) + 1
        return {"total_tickets": len(tickets), "category_counts": categories}
    
    def delete_ticket(self, ticket_id: str):
        if self.use_sqlite:
            self.conn.execute("DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,))
            self.conn.commit()
        else:
            self.collection.delete_one({"ticket_id": ticket_id})

storage = StorageHandler()