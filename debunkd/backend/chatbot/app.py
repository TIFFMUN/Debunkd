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


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import os
from helper import verify_and_correct_statement, teach_deepfakes_and_misinfo, vectorstore, teacher_vectorstore 

# Initialize Flask app
app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s]: %(message)s")

# Dictionary to store conversation history
conversations = {}

@app.route("/")
def serve_home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:filename>")
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/verify", methods=["POST"])
def verify_statement():
    try:
        if request.content_type == "application/json":
            data = request.get_json()
            statement = data.get("text", "").strip()
        else:
            statement = request.form.get("text", "").strip()

        if not statement:
            logging.error("No statement provided in the request")
            return jsonify({"error": "No statement provided"}), 400

        result = verify_and_correct_statement(statement)
        return jsonify({"result": result})

    except Exception as e:
        logging.error(f"Error verifying statement: {e}")
        return jsonify({"error": "An error occurred while verifying the statement"}), 500

@app.route("/chat", methods=["POST"])
def chat():
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

        return jsonify({"response": response, "history": conversations[session_id]})

    except Exception as e:
        logging.error(f"Error processing chat message: {e}")
        return jsonify({"error": "An error occurred while processing the chat message"}), 500

if __name__ == "__main__":
    # Render assigns a port dynamically, so we must use it
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if not set
    logging.info(f"Starting server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
