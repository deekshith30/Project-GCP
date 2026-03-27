from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "USB drive", "price": 1200.0},
    {"id": 2, "name": "Keyboard", "price": 150.0},
    {"id": 3, "name": "HDMI cable", "price": 40.0},
]


@app.get("/health")
def health():
    return {"status": "ok"}, 200


@app.get("/ready")
def ready():
    return {"status": "ready"}, 200


@app.get("/products")
def list_products():
    return jsonify(PRODUCTS), 200


@app.get("/products/<int:product_id>")
def get_product(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return {"error": "Product not found"}, 404
    return jsonify(product), 200


@app.post("/products")
def create_product():
    data = request.get_json() or {}
    if "name" not in data or "price" not in data:
        return {"error": "name and price are required"}, 400

    new_id = max(p["id"] for p in PRODUCTS) + 1
    product = {"id": new_id, "name": data["name"], "price": float(data["price"])}
    PRODUCTS.append(product)
    return jsonify(product), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
