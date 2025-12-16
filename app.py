from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flashing messages

# Database Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['gaming_center_db']
slots_collection = db['slots']

# --- Routes ---

@app.route('/')
def index():
    # Fetch all slots sorted by time (logic simplified for demo)
    slots = list(slots_collection.find())
    return render_template('index.html', slots=slots)

@app.route('/book/<slot_id>', methods=['GET', 'POST'])
def book_slot(slot_id):
    # Find the specific slot
    slot = slots_collection.find_one({"_id": ObjectId(slot_id)})
    
    if not slot:
        return "Slot not found", 404

    if request.method == 'POST':
        customer_name = request.form.get('name')
        
        # Update the database
        slots_collection.update_one(
            {"_id": ObjectId(slot_id)},
            {"$set": {"status": "booked", "booked_by": customer_name}}
        )
        
        flash(f"Slot booked successfully for {customer_name}!")
        return redirect(url_for('index'))

    return render_template('book.html', slot=slot)

@app.route('/cancel/<slot_id>')
def cancel_slot(slot_id):
    # functionality to reset a slot
    slots_collection.update_one(
        {"_id": ObjectId(slot_id)},
        {"$set": {"status": "available", "booked_by": None}}
    )
    flash("Booking cancelled.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)