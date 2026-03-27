from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Keyboard", "price": 1200.0},
    {"id": 2, "name": "USB Drive", "price": 150.0},
    {"id": 3, "name": "HDMI cable", "price": 40.0},
]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/ready", methods=["GET"])
def ready():
    return jsonify({"status": "ready"}), 200


@app.route("/products", methods=["GET"])
def list_products():
    return jsonify(PRODUCTS), 200


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json() or {}
    if "name" not in data or "price" not in data:
        return jsonify({"error": "name and price are required"}), 400

    new_id = max(p["id"] for p in PRODUCTS) + 1 if PRODUCTS else 1
    product = {"id": new_id, "name": data["name"], "price": float(data["price"])}
    PRODUCTS.append(product)
    return jsonify(product), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
