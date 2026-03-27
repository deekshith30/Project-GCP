from flask import Flask, jsonify, request

app = Flask(__name__)

USERS = [
    {"id": 1, "name": "Deekshith"},
    {"id": 2, "name": "Sarves"}
]

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/ready", methods=["GET"])
def ready():
    return jsonify({"status": "ready"}), 200

@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(USERS), 200

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
