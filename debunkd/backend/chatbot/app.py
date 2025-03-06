from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import os
from helper import verify_and_correct_statement  # Import the function from helper.py

# Initialize Flask app
app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# ✅ Serve Frontend (index.html as Homepage)
@app.route("/")
def serve_home():
    return send_from_directory(app.static_folder, "index.html")

# ✅ Serve Static Files (CSS, JS, Images, etc.)
@app.route("/<path:filename>")
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

# ✅ API Endpoint for Misinformation Verification
@app.route("/verify", methods=["POST"])
def verify_statement():
    data = request.json
    statement = data.get("statement")

    if not statement:
        logging.error("No statement provided in the request")
        return jsonify({"error": "No statement provided"}), 400

    try:
        # Call the verify_and_correct_statement function from helper.py
        result = verify_and_correct_statement(statement)
        return jsonify({"result": result})

    except Exception as e:
        logging.error(f"Error verifying statement: {e}")
        return jsonify({"error": "An error occurred while verifying the statement"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Flask runs on localhost:5000
