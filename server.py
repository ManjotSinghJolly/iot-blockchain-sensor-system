from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib, json, os
from blockchain_client import send_hash_to_blockchain  # 👈 Import your blockchain client
from flask import render_template
from datetime import timedelta

app = Flask(__name__)


# ---------------- DATABASE SETUP ----------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'sensor_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    data_hash = db.Column(db.String(64), nullable=False)
    tx_hash = db.Column(db.String(80)) # Transcation hash
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create table if not exists
with app.app_context():
    db.create_all()

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return "IoT Blockchain Backend with Database + Blockchain Integration Running!"

@app.route('/api/sensor', methods=['POST'])
def receive_data():
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            print("⚠️ Raw Data:", request.data)
            return jsonify({"error": "Invalid or empty JSON"}), 415

        temperature = data.get('temperature')
        humidity = data.get('humidity')

        # Compute SHA-256 hash for data integrity
        hash_input = json.dumps(data, sort_keys=True).encode()
        data_hash = hashlib.sha256(hash_input).hexdigest()

        # Send to blockchain
        from blockchain_client import send_hash_to_blockchain
        tx_hash = send_hash_to_blockchain(data_hash)

        # Store data in the local database
        new_entry = SensorData(
            temperature=temperature,
            humidity=humidity,
            data_hash=data_hash,
            tx_hash=tx_hash
        )
        db.session.add(new_entry)
        db.session.commit()

        print(f"Stored: Temp = {temperature}°C, Hum={humidity}%, Hash={data_hash}, TX={tx_hash}")

        return jsonify({
            "status": "success",
            "hash": data_hash,
            "blockchain_tx": tx_hash,
            "timestamp": new_entry.timestamp.isoformat()
        }), 200

    except Exception as e:
        print("❌ Exception:", str(e))
        return jsonify({"error": str(e)}), 500
    
@app.route('/dashboard')
def dashboard():
    records = SensorData.query.order_by(SensorData.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', records=records)

# ---------------- ENTRY POINT ----------------

@app.route("/api/dashboard_data")
def dashboard_data():
    records = SensorData.query.order_by(SensorData.timestamp.desc()).limit(10).all()
    chart_data = {
        "timestamps": [r.timestamp.strftime("%H:%M:%S") for r in reversed(records)],
        "temperature": [r.temperature for r in reversed(records)],
        "humidity": [r.humidity for r in reversed(records)],
    }

    return {
        "latest": {
            "temp": records[0].temperature if records else 0,
            "humidity": records[0].humidity if records else 0
        },
        "records": [
            {
             "hash": r.data_hash,
            "tx": r.tx_hash or "", # For now - we will store real tx hashes soon!
            "time": (r.timestamp + timedelta(hours = 5, minutes = 30)).strftime("%H:%M:%S")
            } for r in records
        ],
        "chart": chart_data
    }
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
