"""
Flask application for PhishGuard: URL analysis, history, and stats routes.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import joblib
from utils.extract_features import extract_features_from_url

app = Flask(__name__)
# Load pre-trained classifier
classifier = joblib.load("model/phishing_model.pkl")

def log_request(original_url: str, result: int):
    conn = sqlite3.connect("phishing.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS history (url TEXT, prediction INTEGER, timestamp TEXT)"
    )
    timestamp = datetime.utcnow().isoformat()
    cur.execute(
        "INSERT INTO history (url, prediction, timestamp) VALUES (?, ?, ?)",
        (original_url, result, timestamp)
    )
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_url():
    payload = request.get_json() or {}
    target = payload.get("url", "")
    features = extract_features_from_url(target)
    if not features:
        return jsonify({"error": "No se pudo procesar la URL."}), 400
    prediction = int(classifier.predict([features])[0])
    log_request(target, prediction)
    return jsonify({"prediction": prediction})

@app.route("/history")
def show_history():
    conn = sqlite3.connect("phishing.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT url, prediction, timestamp FROM history ORDER BY timestamp DESC LIMIT 20"
    )
    entries = cur.fetchall()
    conn.close()
    return render_template("history.html", records=entries)

@app.route("/stats")
def show_stats():
    conn = sqlite3.connect("phishing.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM history")
    total_scans = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM history WHERE prediction=1")
    phishing_count = cur.fetchone()[0]
    legit_count = total_scans - phishing_count
    conn.close()

    return render_template(
        "stats.html", total=total_scans, phishing=phishing_count, legit=legit_count
    )

if __name__ == "__main__":
    app.run(debug=True)
