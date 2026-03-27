from flask import Flask, jsonify, request

app = Flask(__name__)

USERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

@app.get("/health")
def health():
    return {"status": "ok"}, 200

@app.get("/ready")
def ready():
    return {"status": "ready"}, 200

@app.get("/users")
def list_users():
    return jsonify(USERS), 200

@app.get("/users/<int:user_id>")
def get_user(user_id):
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return {"error": "User not found"}, 404
    return jsonify(user), 200

@app.post("/users")
def create_user():
    data = request.get_json() or {}
    if "name" not in data:
        return {"error": "name is required"}, 400

    new_id = max(u["id"] for u in USERS) + 1
    user = {"id": new_id, "name": data["name"]}
    USERS.append(user)
    return jsonify(user), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
