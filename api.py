from flask import Flask, request, jsonify
from ai_processor import generate_reply, extract_sender_name
from sheets_service import save_lead
from datetime import datetime, timezone, timedelta
import os

PKT = timezone(timedelta(hours=5))

app = Flask(__name__)

API_KEY = os.getenv("API_KEY", "change-this-secret-key")


def check_auth(req):
    key = req.headers.get("X-API-Key") or req.args.get("api_key")
    return key == API_KEY


# -----------------------------------------------
# POST /process-email
# Trigger: Zapier, Relevance.ai, Make, or manual
# -----------------------------------------------
@app.route("/process-email", methods=["POST"])
def process_email():

    if not check_auth(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    email_body   = data.get("email_body", "").strip()
    sender_email = data.get("sender_email", "").strip()
    sender_raw   = data.get("sender_raw", sender_email).strip()
    subject      = data.get("subject", "No Subject").strip()

    if not email_body or not sender_email:
        return jsonify({"error": "email_body and sender_email are required"}), 400

    try:
        # generate_reply now returns (reply, category)
        reply, category = generate_reply(email_body)

        # Extract sender name
        sender_name = extract_sender_name(email_body, sender_raw)

        # Save lead — 5 args including category
        timestamp = datetime.now(PKT).strftime("%Y-%m-%d %H:%M:%S")
        save_lead(sender_name, sender_email, email_body, timestamp, category)

        return jsonify({
            "status":       "success",
            "reply":        reply,
            "category":     category,
            "sender_name":  sender_name,
            "sender_email": sender_email,
            "subject":      subject,
            "timestamp":    timestamp,
            "lead_saved":   True
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------------------------
# GET /health
# Quick check that the API is live
# -----------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "AI Customer Support Automation"}), 200


# -----------------------------------------------
# Run locally
# -----------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
