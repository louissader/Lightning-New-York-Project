# Import required libraries
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask application
app = Flask(__name__)

# Configure PostgreSQL database
# Format: postgresql://username:password@localhost:5432/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://louissader@localhost:5432/lny_products'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)


# Product model - represents the products table in PostgreSQL
class Product(db.Model):
    """Model for storing product information."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Price with 2 decimal places
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name}>'


# Log model - represents the logs table for tracking all actions
class Log(db.Model):
    """Model for storing action logs (bonus feature)."""
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    product_price = db.Column(db.Numeric(10, 2))
    product_category = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Log {self.action} - {self.product_name}>'


def log_action(action, product):
    """Log an action (Added/Deleted) with the affected product to the database."""
    log = Log(
        action=action,
        product_name=product.name,
        product_price=product.price,
        product_category=product.category
    )
    db.session.add(log)
    db.session.commit()


@app.route("/")
def index():
    """Display the main page with all products, with optional filtering and sorting."""
    # Get filter and sort parameters from query string
    category_filter = request.args.get('category', '')
    sort_by = request.args.get('sort', '')

    # Build query
    query = Product.query

    # Apply category filter if specified
    if category_filter:
        query = query.filter(Product.category == category_filter)

    # Apply sorting if specified
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    products = query.all()

    # Get all unique categories for the filter dropdown
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]

    return render_template("index.html", products=products, categories=categories,
                         selected_category=category_filter, selected_sort=sort_by)


@app.route("/add", methods=["GET", "POST"])
def add_product():
    """Handle adding new products. GET shows form, POST processes submission."""
    if request.method == "POST":
        # Get form data
        name = request.form["name"]
        price = request.form["price"]
        category = request.form["category"]

        # Create new product entry
        new_product = Product(
            name=name,
            price=price,
            category=category
        )

        # Add to database
        db.session.add(new_product)
        db.session.commit()

        # Log the action
        log_action("Added", new_product)

        # Redirect to main page
        return redirect(url_for("index"))

    # Show add product form for GET requests
    return render_template("add_product.html")


@app.route("/delete/<int:product_id>")
def delete_product(product_id):
    """Delete a product by its ID."""
    product = Product.query.get(product_id)

    if product:
        # Log before deleting
        log_action("Deleted", product)

        # Delete from database
        db.session.delete(product)
        db.session.commit()

    return redirect(url_for("index"))


@app.route("/logs")
def logs():
    """Display all logged actions (bonus feature)."""
    all_logs = Log.query.order_by(Log.timestamp.desc()).all()
    return render_template("logs.html", logs=all_logs)


# Run the Flask application in debug mode
if __name__ == "__main__":
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)
