import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from nlp_processor import analyze_complaint
from report_generator import generate_report
from destination_finder import recommend_destinations

load_dotenv()
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    complaint = (data.get("complaint") or "").strip()
    if len(complaint) < 12:
        return jsonify({"error": "Please describe the problem in at least a few words."}), 400
    if len(complaint) > 5000:
        return jsonify({"error": "Please keep the complaint under 5,000 characters."}), 400

    analysis = analyze_complaint(complaint)
    try:
        report = generate_report(complaint, analysis)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502

    destinations = recommend_destinations(analysis["category"], complaint)
    return jsonify({
        "analysis": analysis,
        "report": report,
        "destinations": destinations
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
