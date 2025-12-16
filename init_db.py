from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['gaming_center_db']
slots_collection = db['slots']

def init_slots():
    # Clear existing slots to avoid duplicates for this demo
    slots_collection.delete_many({})

    # Create dummy slots for a single day (e.g., 10 AM to 8 PM)
    slots = []
    times = ["10:00 AM", "11:00 AM", "12:00 PM", "01:00 PM", 
             "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM", "06:00 PM"]
    
    for time in times:
        slots.append({
            "time": time,
            "status": "available",  # Options: available, booked
            "booked_by": None,
            "console_type": "PS5"   # You can add types like PC, PS5, Xbox
        })

    slots_collection.insert_many(slots)
    print("Database initialized with empty slots!")

if __name__ == "__main__":
    init_slots()