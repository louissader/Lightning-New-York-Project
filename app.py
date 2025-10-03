# Import required libraries
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import logging
from functools import wraps

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

# Configure logging (important for production applications)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


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


@app.route("/api-docs")
def api_docs():
    """Display API documentation (like Swagger)."""
    return render_template("api_docs.html")


# ============================================================================
# REST API ENDPOINTS
# ============================================================================
# These endpoints demonstrate REST API design, JSON handling, and HTTP methods
# Skills required for Python developer role: Flask, REST APIs, JSON, error handling

def validate_product_data(data):
    """Validate product data for API requests."""
    errors = []

    if not data.get('name'):
        errors.append("Product name is required")
    elif len(data.get('name', '')) > 200:
        errors.append("Product name must be 200 characters or less")

    if not data.get('price'):
        errors.append("Price is required")
    else:
        try:
            price = float(data.get('price'))
            if price < 0:
                errors.append("Price must be a positive number")
        except (ValueError, TypeError):
            errors.append("Price must be a valid number")

    if not data.get('category'):
        errors.append("Category is required")
    elif len(data.get('category', '')) > 100:
        errors.append("Category must be 100 characters or less")

    return errors


@app.route("/api/products", methods=["GET"])
def api_get_products():
    """
    GET /api/products - Retrieve all products with optional filtering
    Query params: category (optional), sort (optional: price_asc, price_desc)
    Returns: JSON array of products
    """
    try:
        category_filter = request.args.get('category', '')
        sort_by = request.args.get('sort', '')

        query = Product.query

        # Apply filters
        if category_filter:
            query = query.filter(Product.category == category_filter)

        # Apply sorting
        if sort_by == 'price_asc':
            query = query.order_by(Product.price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Product.price.desc())
        else:
            query = query.order_by(Product.created_at.desc())

        products = query.all()

        # Convert to JSON-serializable format
        products_data = [{
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'category': p.category,
            'created_at': p.created_at.isoformat()
        } for p in products]

        logger.info(f"API: Retrieved {len(products_data)} products")

        return jsonify({
            'success': True,
            'count': len(products_data),
            'data': products_data
        }), 200

    except Exception as e:
        logger.error(f"API Error retrieving products: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve products'
        }), 500


@app.route("/api/products/<int:product_id>", methods=["GET"])
def api_get_product(product_id):
    """
    GET /api/products/<id> - Retrieve a single product by ID
    Returns: JSON object with product details
    """
    try:
        product = Product.query.get(product_id)

        if not product:
            return jsonify({
                'success': False,
                'error': 'Product not found'
            }), 404

        product_data = {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'category': product.category,
            'created_at': product.created_at.isoformat()
        }

        logger.info(f"API: Retrieved product {product_id}")

        return jsonify({
            'success': True,
            'data': product_data
        }), 200

    except Exception as e:
        logger.error(f"API Error retrieving product {product_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve product'
        }), 500


@app.route("/api/products", methods=["POST"])
def api_create_product():
    """
    POST /api/products - Create a new product
    Body: JSON with name, price, category
    Returns: JSON with created product details
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400

        # Validate data
        errors = validate_product_data(data)
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400

        # Create new product
        new_product = Product(
            name=data['name'],
            price=data['price'],
            category=data['category']
        )

        db.session.add(new_product)
        db.session.commit()

        # Log the action
        log_action("Added", new_product)

        product_data = {
            'id': new_product.id,
            'name': new_product.name,
            'price': float(new_product.price),
            'category': new_product.category,
            'created_at': new_product.created_at.isoformat()
        }

        logger.info(f"API: Created product {new_product.id} - {new_product.name}")

        return jsonify({
            'success': True,
            'message': 'Product created successfully',
            'data': product_data
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"API Error creating product: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to create product'
        }), 500


@app.route("/api/products/<int:product_id>", methods=["PUT"])
def api_update_product(product_id):
    """
    PUT /api/products/<id> - Update an existing product
    Body: JSON with fields to update (name, price, category)
    Returns: JSON with updated product details
    """
    try:
        product = Product.query.get(product_id)

        if not product:
            return jsonify({
                'success': False,
                'error': 'Product not found'
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400

        # Validate data
        errors = validate_product_data(data)
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400

        # Update product
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.category = data.get('category', product.category)

        db.session.commit()

        product_data = {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'category': product.category,
            'created_at': product.created_at.isoformat()
        }

        logger.info(f"API: Updated product {product_id}")

        return jsonify({
            'success': True,
            'message': 'Product updated successfully',
            'data': product_data
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"API Error updating product {product_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to update product'
        }), 500


@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def api_delete_product(product_id):
    """
    DELETE /api/products/<id> - Delete a product
    Returns: JSON confirmation message
    """
    try:
        product = Product.query.get(product_id)

        if not product:
            return jsonify({
                'success': False,
                'error': 'Product not found'
            }), 404

        # Log before deleting
        log_action("Deleted", product)

        db.session.delete(product)
        db.session.commit()

        logger.info(f"API: Deleted product {product_id}")

        return jsonify({
            'success': True,
            'message': 'Product deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"API Error deleting product {product_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to delete product'
        }), 500


@app.route("/api/export/products", methods=["GET"])
def api_export_products():
    """
    GET /api/export/products - Export products data
    Query params: format (json or csv), category (optional filter)
    Returns: Products data in requested format

    Demonstrates ETL capabilities - extracting data for integration with other systems
    """
    try:
        export_format = request.args.get('format', 'json').lower()
        category_filter = request.args.get('category', '')

        query = Product.query

        if category_filter:
            query = query.filter(Product.category == category_filter)

        products = query.order_by(Product.created_at.desc()).all()

        if export_format == 'csv':
            # CSV export for ETL/data pipeline use cases
            import io
            import csv

            output = io.StringIO()
            writer = csv.writer(output)

            # Write header
            writer.writerow(['ID', 'Name', 'Price', 'Category', 'Created At'])

            # Write data
            for p in products:
                writer.writerow([
                    p.id,
                    p.name,
                    float(p.price),
                    p.category,
                    p.created_at.isoformat()
                ])

            csv_data = output.getvalue()

            logger.info(f"API: Exported {len(products)} products as CSV")

            return csv_data, 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': 'attachment; filename=products_export.csv'
            }

        else:  # JSON format (default)
            products_data = [{
                'id': p.id,
                'name': p.name,
                'price': float(p.price),
                'category': p.category,
                'created_at': p.created_at.isoformat()
            } for p in products]

            logger.info(f"API: Exported {len(products)} products as JSON")

            return jsonify({
                'success': True,
                'count': len(products_data),
                'data': products_data,
                'exported_at': datetime.utcnow().isoformat()
            }), 200

    except Exception as e:
        logger.error(f"API Error exporting products: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to export products'
        }), 500


@app.route("/api/stats", methods=["GET"])
def api_get_stats():
    """
    GET /api/stats - Get database statistics
    Returns: JSON with product statistics and metrics

    Demonstrates SQL aggregation and database optimization skills
    """
    try:
        # Get total products
        total_products = Product.query.count()

        # Get products by category
        category_stats = db.session.query(
            Product.category,
            db.func.count(Product.id).label('count'),
            db.func.avg(Product.price).label('avg_price'),
            db.func.sum(Product.price).label('total_value')
        ).group_by(Product.category).all()

        category_data = [{
            'category': stat.category,
            'count': stat.count,
            'average_price': float(stat.avg_price) if stat.avg_price else 0,
            'total_value': float(stat.total_value) if stat.total_value else 0
        } for stat in category_stats]

        # Get recent activity from logs
        recent_logs = Log.query.order_by(Log.timestamp.desc()).limit(10).all()

        recent_activity = [{
            'action': log.action,
            'product_name': log.product_name,
            'timestamp': log.timestamp.isoformat()
        } for log in recent_logs]

        logger.info("API: Retrieved statistics")

        return jsonify({
            'success': True,
            'data': {
                'total_products': total_products,
                'categories': category_data,
                'recent_activity': recent_activity
            }
        }), 200

    except Exception as e:
        logger.error(f"API Error retrieving stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve statistics'
        }), 500


# Run the Flask application in debug mode
if __name__ == "__main__":
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)
