# Import required libraries
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from dotenv import load_dotenv
from time import time
import os
import logging
from functools import wraps

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Security Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['WTF_CSRF_ENABLED'] = True

# Configure PostgreSQL database from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://louissader@localhost:5432/lny_products'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
)

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


# ============================================================================
# DATABASE MODELS
# ============================================================================

class Product(db.Model):
    """Model for storing product information with database indexes for performance."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Database indexes for query optimization
    __table_args__ = (
        db.Index('idx_category', 'category'),
        db.Index('idx_price', 'price'),
        db.Index('idx_created_at', 'created_at'),
    )

    def __repr__(self):
        return f'<Product {self.name}>'

    def to_dict(self):
        """Convert product to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price),
            'category': self.category,
            'created_at': self.created_at.isoformat()
        }


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


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

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


def log_performance(f):
    """Decorator to log function execution time for performance monitoring."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time()
        result = f(*args, **kwargs)
        end_time = time()
        logger.info(f"{f.__name__} executed in {end_time - start_time:.3f}s")
        return result
    return decorated_function


def require_api_key(f):
    """Decorator to require API key authentication for endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        expected_key = os.getenv('API_KEY')

        if not expected_key or api_key != expected_key:
            logger.warning(f"Unauthorized API access attempt from {request.remote_addr}")
            return jsonify({
                'success': False,
                'error': 'Invalid or missing API key'
            }), 401

        return f(*args, **kwargs)
    return decorated_function


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


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Endpoint not found'}), 404
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    db.session.rollback()  # Rollback any failed database transactions
    logger.error(f"Internal server error: {str(error)}")

    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
    return render_template('500.html'), 500


@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded errors."""
    return jsonify({
        'success': False,
        'error': 'Rate limit exceeded. Please try again later.'
    }), 429


# ============================================================================
# WEB INTERFACE ROUTES
# ============================================================================

@app.route("/")
@log_performance
def index():
    """Display the main page with all products, with optional filtering and sorting."""
    category_filter = request.args.get('category', '')
    sort_by = request.args.get('sort', '')

    query = Product.query

    if category_filter:
        query = query.filter(Product.category == category_filter)

    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    products = query.all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]

    return render_template("index.html", products=products, categories=categories,
                         selected_category=category_filter, selected_sort=sort_by)


@app.route("/add", methods=["GET", "POST"])
def add_product():
    """Handle adding new products. GET shows form, POST processes submission."""
    if request.method == "POST":
        from markupsafe import escape

        # Sanitize inputs to prevent XSS
        name = escape(request.form["name"].strip())
        price = request.form["price"]
        category = escape(request.form["category"].strip())

        # Validate
        if not name or not price or not category:
            return render_template("add_product.html",
                                 error="All fields are required"), 400

        try:
            price = float(price)
            if price < 0:
                return render_template("add_product.html",
                                     error="Price must be positive"), 400
        except ValueError:
            return render_template("add_product.html",
                                 error="Invalid price format"), 400

        new_product = Product(
            name=str(name),
            price=price,
            category=str(category)
        )

        db.session.add(new_product)
        db.session.commit()
        log_action("Added", new_product)

        logger.info(f"Product added: {new_product.name} (ID: {new_product.id})")

        return redirect(url_for("index"))

    return render_template("add_product.html")


@app.route("/delete/<int:product_id>")
def delete_product(product_id):
    """Delete a product by its ID."""
    product = Product.query.get(product_id)

    if product:
        log_action("Deleted", product)
        logger.info(f"Product deleted: {product.name} (ID: {product.id})")

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

@app.route("/api/products", methods=["GET"])
@limiter.limit("30 per minute")
@csrf.exempt  # CSRF not needed for GET requests
@log_performance
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

        if category_filter:
            query = query.filter(Product.category == category_filter)

        if sort_by == 'price_asc':
            query = query.order_by(Product.price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Product.price.desc())
        else:
            query = query.order_by(Product.created_at.desc())

        products = query.all()
        products_data = [p.to_dict() for p in products]

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
@limiter.limit("30 per minute")
@csrf.exempt
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

        logger.info(f"API: Retrieved product {product_id}")

        return jsonify({
            'success': True,
            'data': product.to_dict()
        }), 200

    except Exception as e:
        logger.error(f"API Error retrieving product {product_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve product'
        }), 500


@app.route("/api/products", methods=["POST"])
@limiter.limit("10 per minute")
@csrf.exempt  # CSRF exempt for API
@require_api_key  # Require API key for write operations
def api_create_product():
    """
    POST /api/products - Create a new product
    Body: JSON with name, price, category
    Returns: JSON with created product details
    Requires: X-API-Key header
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400

        errors = validate_product_data(data)
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400

        new_product = Product(
            name=data['name'],
            price=data['price'],
            category=data['category']
        )

        db.session.add(new_product)
        db.session.commit()
        log_action("Added", new_product)

        logger.info(f"API: Created product {new_product.id} - {new_product.name}")

        return jsonify({
            'success': True,
            'message': 'Product created successfully',
            'data': new_product.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"API Error creating product: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to create product'
        }), 500


@app.route("/api/products/<int:product_id>", methods=["PUT"])
@limiter.limit("10 per minute")
@csrf.exempt
@require_api_key
def api_update_product(product_id):
    """
    PUT /api/products/<id> - Update an existing product
    Body: JSON with fields to update (name, price, category)
    Returns: JSON with updated product details
    Requires: X-API-Key header
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

        errors = validate_product_data(data)
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400

        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.category = data.get('category', product.category)

        db.session.commit()

        logger.info(f"API: Updated product {product_id}")

        return jsonify({
            'success': True,
            'message': 'Product updated successfully',
            'data': product.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"API Error updating product {product_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to update product'
        }), 500


@app.route("/api/products/<int:product_id>", methods=["DELETE"])
@limiter.limit("10 per minute")
@csrf.exempt
@require_api_key
def api_delete_product(product_id):
    """
    DELETE /api/products/<id> - Delete a product
    Returns: JSON confirmation message
    Requires: X-API-Key header
    """
    try:
        product = Product.query.get(product_id)

        if not product:
            return jsonify({
                'success': False,
                'error': 'Product not found'
            }), 404

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
@limiter.limit("20 per minute")
@csrf.exempt
@log_performance
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
            import io
            import csv

            output = io.StringIO()
            writer = csv.writer(output)

            writer.writerow(['ID', 'Name', 'Price', 'Category', 'Created At'])

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

        else:
            products_data = [p.to_dict() for p in products]

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
@limiter.limit("20 per minute")
@csrf.exempt
@log_performance
def api_get_stats():
    """
    GET /api/stats - Get database statistics
    Returns: JSON with product statistics and metrics

    Demonstrates SQL aggregation and database optimization skills
    """
    try:
        total_products = Product.query.count()

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


# Run the Flask application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    debug_mode = os.getenv('DEBUG', 'True').lower() == 'true'
    app.run(debug=debug_mode)
