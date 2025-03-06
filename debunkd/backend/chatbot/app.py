from flask import Flask, request, jsonify
from flask_cors import CORS
from helper import verify_and_correct_statement  # Import the function from helper.py
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
    app.run(debug=True)