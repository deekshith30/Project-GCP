from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory cart storage: { user_id: [ {product_id, quantity}, ... ] }
CARTS = {}


@app.get("/health")
def health():
    return {"status": "ok"}, 200


@app.get("/ready")
def ready():
    return {"status": "ready"}, 200


@app.get("/cart/<int:user_id>")
def get_cart(user_id):
    return {"user_id": user_id, "items": CARTS.get(user_id, [])}, 200


@app.post("/cart/<int:user_id>/items")
def add_item(user_id):
    data = request.get_json() or {}
    if "product_id" not in data or "quantity" not in data:
        return {"error": "product_id and quantity are required"}, 400

    product_id = int(data["product_id"])
    quantity = int(data["quantity"])

    items = CARTS.get(user_id, [])
    existing = next((i for i in items if i["product_id"] == product_id), None)

    if existing:
        existing["quantity"] += quantity
    else:
        items.append({"product_id": product_id, "quantity": quantity})

    CARTS[user_id] = items
    return {"user_id": user_id, "items": items}, 201


@app.delete("/cart/<int:user_id>/items/<int:product_id>")
def remove_item(user_id, product_id):
    items = CARTS.get(user_id, [])
    items = [i for i in items if i["product_id"] != product_id]
    CARTS[user_id] = items
    return {"user_id": user_id, "items": items}, 200


@app.post("/cart/<int:user_id>/clear")
def clear_cart(user_id):
    CARTS[user_id] = []
    return {"user_id": user_id, "items": []}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
