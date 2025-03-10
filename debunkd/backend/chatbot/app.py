# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import logging
# import os
# from helper import verify_and_correct_statement, teach_deepfakes_and_misinfo, vectorstore, teacher_vectorstore 
# app = Flask(__name__, static_folder="../frontend", static_url_path="")
# CORS(app)

# logging.basicConfig(level=logging.DEBUG)
# conversations = {}
# @app.route("/")
# def serve_home():
#     return send_from_directory(app.static_folder, "index.html")

# @app.route("/<path:filename>")
# def serve_static_files(filename):
#     return send_from_directory(app.static_folder, filename)

# @app.route("/verify", methods=["POST"])
# def verify_statement():
#     try:
#         if request.content_type == "application/json":
#             data = request.get_json()
#             statement = data.get("text", "").strip()
#         else:
#             statement = request.form.get("text", "").strip()

#         if not statement:
#             logging.error("No statement provided in the request")
#             return jsonify({"error": "No statement provided"}), 400

#         result = verify_and_correct_statement(statement)
#         return jsonify({"result": result})

#     except Exception as e:
#         logging.error(f"Error verifying statement: {e}")
#         return jsonify({"error": "An error occurred while verifying the statement"}), 500

# @app.route("/chat", methods=["POST"])
# def chat():
#     try:
#         data = request.get_json()
#         if not data or "message" not in data:
#             logging.error("No message provided in the request")
#             return jsonify({"error": "No message provided"}), 400
#         message = data["message"].strip()
#         session_id = data.get("session_id", "default")
#         if session_id not in conversations:
#             conversations[session_id] = []

#         conversations[session_id].append({"role": "user", "content": message})
#         history_context = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in conversations[session_id]]
#         )
#         response = teach_deepfakes_and_misinfo(message, history_context)
#         conversations[session_id].append({"role": "assistant", "content": response})

#         return jsonify({"response": response, "history": conversations[session_id]})

#     except Exception as e:
#         logging.error(f"Error processing chat message: {e}")
#         return jsonify({"error": "An error occurred while processing the chat message"}), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)

# vers 2

# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import logging
# import os

# # Import helper functions safely
# try:
#     from helper import verify_and_correct_statement, teach_deepfakes_and_misinfo
# except ImportError as e:
#     logging.error(f"Error importing helper functions: {e}")
#     verify_and_correct_statement = None
#     teach_deepfakes_and_misinfo = None

# # Initialize Flask app
# app = Flask(__name__, static_folder="../frontend", static_url_path="")
# CORS(app)

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s]: %(message)s")

# # Dictionary to store conversation history
# conversations = {}

# @app.route("/")
# def serve_home():
#     """Serve the frontend index.html"""
#     return send_from_directory(app.static_folder, "index.html")

# @app.route("/<path:filename>")
# def serve_static_files(filename):
#     """Serve other frontend static files"""
#     return send_from_directory(app.static_folder, filename)

# @app.route("/verify", methods=["POST"])
# def verify_statement():
#     """Handles fact verification"""
#     if verify_and_correct_statement is None:
#         logging.error("verify_and_correct_statement function not found.")
#         return jsonify({"error": "Server misconfiguration"}), 500

#     try:
#         data = request.get_json() if request.content_type == "application/json" else request.form
#         statement = data.get("text", "").strip()

#         if not statement:
#             logging.error("No statement provided in the request")
#             return jsonify({"error": "No statement provided"}), 400

#         result = verify_and_correct_statement(statement)
#         return jsonify({"result": result})

#     except Exception as e:
#         logging.error(f"Error verifying statement: {e}")
#         return jsonify({"error": "An error occurred while verifying the statement"}), 500

# @app.route("/chat", methods=["POST"])
# def chat():
#     """Handles chatbot messages"""
#     if teach_deepfakes_and_misinfo is None:
#         logging.error("teach_deepfakes_and_misinfo function not found.")
#         return jsonify({"error": "Server misconfiguration"}), 500

#     try:
#         data = request.get_json()
#         if not data or "message" not in data:
#             logging.error("No message provided in the request")
#             return jsonify({"error": "No message provided"}), 400

#         message = data["message"].strip()
#         session_id = data.get("session_id", "default")

#         if session_id not in conversations:
#             conversations[session_id] = []

#         conversations[session_id].append({"role": "user", "content": message})
#         history_context = "\n".join(
#             [f"{msg['role']}: {msg['content']}" for msg in conversations[session_id]]
#         )
#         response = teach_deepfakes_and_misinfo(message, history_context)
#         conversations[session_id].append({"role": "assistant", "content": response})

#         return jsonify({"response": response, "history": conversations[session_id]})

#     except Exception as e:
#         logging.error(f"Error processing chat message: {e}")
#         return jsonify({"error": "An error occurred while processing the chat message"}), 500

# # Ensure Render detects Flask and binds to the correct port
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 10000))  # Get port dynamically from Render
#     print(f"🚀 Starting Flask app on http://0.0.0.0:{port}/")  # Debugging info

#     try:
#         app.run(host="0.0.0.0", port=port, debug=False)  # Ensure it's not in debug mode on Render
#     except Exception as e:
#         print(f"🔥 ERROR: Flask failed to start on port {port}: {e}")

#vers 3

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import os

# Import helper functions safely
try:
    from helper import verify_and_correct_statement, teach_deepfakes_and_misinfo
except ImportError as e:
    logging.error(f"Error importing helper functions: {e}")
    verify_and_correct_statement = None
    teach_deepfakes_and_misinfo = None

# Initialize Flask app
app = Flask(__name__, static_folder="../frontend", static_url_path="")

# ✅ Allow only Vercel frontend to access the API
CORS(app, resources={r"/*": {"origins": "https://debunkd-six.vercel.app"}})

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s]: %(message)s")

# Dictionary to store conversation history
conversations = {}

@app.route("/")
def serve_home():
    """Serve the frontend index.html"""
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:filename>")
def serve_static_files(filename):
    """Serve other frontend static files"""
    return send_from_directory(app.static_folder, filename)

@app.route("/verify", methods=["POST"])
def verify_statement():
    """Handles fact verification"""
    if verify_and_correct_statement is None:
        logging.error("verify_and_correct_statement function not found.")
        return jsonify({"error": "Server misconfiguration"}), 500

    try:
        data = request.get_json() if request.content_type == "application/json" else request.form
        statement = data.get("text", "").strip()

        if not statement:
            logging.error("No statement provided in the request")
            return jsonify({"error": "No statement provided"}), 400

        result = verify_and_correct_statement(statement)
        response = jsonify({"result": result})
        response.headers.add("Access-Control-Allow-Origin", "https://debunkd-six.vercel.app")  # ✅ Allow Frontend
        return response

    except Exception as e:
        logging.error(f"Error verifying statement: {e}")
        return jsonify({"error": "An error occurred while verifying the statement"}), 500

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chatbot messages"""
    if teach_deepfakes_and_misinfo is None:
        logging.error("teach_deepfakes_and_misinfo function not found.")
        return jsonify({"error": "Server misconfiguration"}), 500

    try:
        data = request.get_json()
        if not data or "message" not in data:
            logging.error("No message provided in the request")
            return jsonify({"error": "No message provided"}), 400

        message = data["message"].strip()
        session_id = data.get("session_id", "default")

        if session_id not in conversations:
            conversations[session_id] = []

        conversations[session_id].append({"role": "user", "content": message})
        history_context = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in conversations[session_id]]
        )
        response = teach_deepfakes_and_misinfo(message, history_context)
        conversations[session_id].append({"role": "assistant", "content": response})

        api_response = jsonify({"response": response, "history": conversations[session_id]})
        api_response.headers.add("Access-Control-Allow-Origin", "https://debunkd-six.vercel.app")  # ✅ Allow Frontend
        return api_response

    except Exception as e:
        logging.error(f"Error processing chat message: {e}")
        return jsonify({"error": "An error occurred while processing the chat message"}), 500

# Ensure Render detects Flask and binds to the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Get port dynamically from Render
    print(f"🚀 Starting Flask app on http://0.0.0.0:{port}/")  # Debugging info

    try:
        app.run(host="0.0.0.0", port=port, debug=False)  # Ensure it's not in debug mode on Render
    except Exception as e:
        print(f"🔥 ERROR: Flask failed to start on port {port}: {e}")
