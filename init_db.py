import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Connect to Atlas
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("No MONGO_URI found! Did you create the .env file?")

client = MongoClient(mongo_uri)
db = client['gaming_center_db']
slots_collection = db['slots']

def init_slots():
    print("Clearing old data...")
    slots_collection.delete_many({})

    print("Creating new slots...")
    slots = []
    # 10 AM to 8 PM
    times = ["10:00 AM", "11:00 AM", "12:00 PM", "01:00 PM", 
             "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM", "06:00 PM"]
    
    for time in times:
        slots.append({
            "time": time,
            "status": "available", 
            "booked_by": None,
            "console_type": "PS5" 
        })

    slots_collection.insert_many(slots)
    print("SUCCESS: Cloud Database initialized with empty slots!")

if __name__ == "__main__":
    init_slots()