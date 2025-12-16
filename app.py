import os
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

# 1. Load the secret password from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

# 2. Secure Database Connection
mongo_uri = os.getenv("MONGO_URI")

# specific check to ensure .env is read correctly
if not mongo_uri:
    raise ValueError("No MONGO_URI found! Did you create the .env file?")

client = MongoClient(mongo_uri)
db = client['gaming_center_db']
slots_collection = db['slots']

# --- Routes ---

@app.route('/')
def index():
    # Fetch all slots
    slots = list(slots_collection.find())
    return render_template('index.html', slots=slots)

@app.route('/book/<slot_id>', methods=['GET', 'POST'])
def book_slot(slot_id):
    slot = slots_collection.find_one({"_id": ObjectId(slot_id)})
    
    if not slot:
        return "Slot not found", 404

    if request.method == 'POST':
        customer_name = request.form.get('name')
        
        # Update database to "booked"
        slots_collection.update_one(
            {"_id": ObjectId(slot_id)},
            {"$set": {"status": "booked", "booked_by": customer_name}}
        )
        
        flash(f"Slot booked successfully for {customer_name}!")
        return redirect(url_for('index'))

    return render_template('book.html', slot=slot)

@app.route('/cancel/<slot_id>')
def cancel_slot(slot_id):
    # Reset slot to available
    slots_collection.update_one(
        {"_id": ObjectId(slot_id)},
        {"$set": {"status": "available", "booked_by": None}}
    )
    flash("Booking cancelled.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)