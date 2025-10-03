import json
import os
from flask import Flask, render_template, request, redirect, url_for

# Initialize Flask application
app = Flask(__name__)

DATA_FILE = "products.json"
LOG_FILE = "logs.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def log_action(action, product):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    logs.append({"action": action, "product": product})
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)


@app.route("/")
def index():
    products = load_data()
    return render_template("index.html", products=products)


@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        quantity = request.form["quantity"]

        new_product = {"name": name, "category": category, "quantity": quantity}
        products = load_data()
        products.append(new_product)
        save_data(products)
        log_action("Added", new_product)

        return redirect(url_for("index"))

    return render_template("add_product.html")


@app.route("/delete/<int:index>")
def delete_product(index):
    products = load_data()
    if 0 <= index < len(products):
        removed = products.pop(index)
        save_data(products)
        log_action("Deleted", removed)
    return redirect(url_for("index"))


@app.route("/logs")
def logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    return render_template("logs.html", logs=logs)


if __name__ == "__main__":
    app.run(debug=True)
