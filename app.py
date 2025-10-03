# Import required libraries
import json
import os
from flask import Flask, render_template, request, redirect, url_for

# Initialize Flask application
app = Flask(__name__)

# Define file paths for data storage
DATA_FILE = "products.json"
LOG_FILE = "logs.json"


def load_data():
    """Load product data from JSON file. Returns empty list if file doesn't exist."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_data(data):
    """Save product data to JSON file with pretty formatting."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def log_action(action, product):
    """Log an action (Added/Deleted) with the affected product to the log file."""
    logs = []
    # Load existing logs if file exists
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    # Append new log entry
    logs.append({"action": action, "product": product})
    # Save updated logs
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)


@app.route("/")
def index():
    """Display the main page with all products."""
    products = load_data()
    return render_template("index.html", products=products)


@app.route("/add", methods=["GET", "POST"])
def add_product():
    """Handle adding new products. GET shows form, POST processes submission."""
    if request.method == "POST":
        # Get form data
        name = request.form["name"]
        category = request.form["category"]
        quantity = request.form["quantity"]

        # Create new product entry
        new_product = {"name": name, "category": category, "quantity": quantity}
        products = load_data()
        products.append(new_product)
        save_data(products)
        log_action("Added", new_product)

        # Redirect to main page
        return redirect(url_for("index"))

    # Show add product form for GET requests
    return render_template("add_product.html")


@app.route("/delete/<int:index>")
def delete_product(index):
    """Delete a product by its index in the list."""
    products = load_data()
    # Verify index is valid before deleting
    if 0 <= index < len(products):
        removed = products.pop(index)
        save_data(products)
        log_action("Deleted", removed)
    return redirect(url_for("index"))


@app.route("/logs")
def logs():
    """Display all logged actions."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    return render_template("logs.html", logs=logs)


# Run the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)
