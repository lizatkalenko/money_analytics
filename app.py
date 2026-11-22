from flask import Flask, request, jsonify
import storage
import logic

app = Flask(__name__)
storage.init()


@app.get("/payments")
def list_payments():
    category = request.args.get("category")
    return jsonify(storage.load(category))


@app.post("/payments")
def add_payment():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "очікується JSON"}), 400

    for field in ("name", "category", "amount", "due_date", "status"):
        if field not in data:
            return jsonify({"error": f"немає поля {field}"}), 400

    try:
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "amount має бути числом"}), 400

    if amount < 0:
        return jsonify({"error": "сума не може бути від'ємною"}), 400

    payment = {
        "name": data["name"],
        "category": data["category"],
        "amount": amount,
        "due_date": data["due_date"],
        "status": data["status"]
    }

    new_id = storage.add(payment)
    return jsonify({"id": new_id}), 201


@app.delete("/payments/<int:payment_id>")
def delete_payment(payment_id):
    if storage.delete_payment(payment_id):
        return jsonify({"deleted": payment_id})

    return jsonify({"error": "платіж не знайдено"}), 404

@app.put("/payments/<int:payment_id>")
def edit_payment(payment_id):
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "очікується JSON"}), 400

    allowed_fields = ("name", "category", "amount", "due_date", "status")

    if len(data) != 1:
        return jsonify({"error": "потрібно передати одне поле"}), 400

    field = next(iter(data))

    if field not in allowed_fields:
        return jsonify({"error": "невідоме поле"}), 400

    value = data[field]

    if field == "amount":
        try:
            value = float(value)
        except (ValueError, TypeError):
            return jsonify({"error": "amount має бути числом"}), 400

        if value < 0:
            return jsonify({"error": "сума не може бути від'ємною"}), 400

    if storage.update_payment(payment_id, field, value):
        return jsonify({"updated": payment_id})

    return jsonify({"error": "платіж не знайдено"}), 404

@app.get("/report")
def report():
    records = storage.load()
    return jsonify(logic.make_report(records))


if __name__ == "__main__":
    app.run(debug=True)
