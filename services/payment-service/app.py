from flask import Flask, jsonify, request
import random
import time

app = Flask(__name__)

PAYMENTS = []


@app.get("/health")
def health():
    return {"status": "ok"}, 200


@app.get("/ready")
def ready():
    return {"status": "ready"}, 200


@app.get("/payments")
def list_payments():
    return jsonify(PAYMENTS), 200


@app.post("/payments")
def create_payment():
    data = request.get_json() or {}
    required = ["user_id", "amount", "currency"]

    if any(field not in data for field in required):
        return {"error": f"{', '.join(required)} are required"}, 400

    time.sleep(0.5)  # simulate processing

    amount = float(data["amount"])
    status = "failed" if amount > 10000 else random.choice(["succeeded", "failed"])

    payment = {
        "id": len(PAYMENTS) + 1,
        "user_id": int(data["user_id"]),
        "amount": amount,
        "currency": data["currency"],
        "status": status,
    }

    PAYMENTS.append(payment)

    return jsonify(payment), 201 if status == "succeeded" else 402


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
