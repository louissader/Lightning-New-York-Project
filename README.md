# Product Management System - LNY Interview Project

> A production-ready Flask application demonstrating professional Python development skills for the Junior Python Developer role at Lighting New York

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## 👋 Thank You

Thank you for taking the time to review my interview project. I've built this application to demonstrate not only my ability to meet the project requirements, but also to showcase the production-ready skills and professional development practices I would bring to the Lighting New York team. I look forward to discussing my approach and technical decisions with you!

---

## 🚀 Quick Start - Running the Application

### Option 1: Using Docker (Recommended)
```bash
# Start everything with one command
docker-compose up

# Access the application
open http://localhost:5000
```

### Option 2: Local Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env

# 3. Create PostgreSQL database
psql postgres -c "CREATE DATABASE lny_products;"

# 4. Run the application
./run.sh

# Access at http://localhost:5000
```

### Optional: FastAPI Server
```bash
# Run FastAPI alongside Flask (port 8000)
./run_fastapi.sh

# Interactive docs: http://localhost:8000/docs
```

---

## ✅ Core Requirements - How I Met Each Requirement

### Required: Product Management Application
**Requirement**: Build an application where users can enter products through a form and view them in a table.

**Implementation**:
- ✅ **Web interface** at http://localhost:5000 with navigation
- ✅ **Add Product form** at `/add` with product name, price, and category fields
- ✅ **Product listing page** at `/` displaying all products in a table format
- ✅ **Python/Flask** framework as required

### Required: Product Attributes
**Requirement**: Each product must include Name, Price, Category, and Created At.

**Implementation**:
- ✅ **Name** - Text field with validation
- ✅ **Price** - Numeric field (float) with validation
- ✅ **Category** - Dropdown selector with 10 lighting categories (Chandeliers, Pendant Lights, etc.)
- ✅ **Created At** - Automatically timestamped when product is added

### Required: Filter by Category
**Requirement**: Allow filtering products by category.

**Implementation**:
- ✅ **Category filter dropdown** on the main product listing page
- ✅ **Filter button** to apply category selection
- ✅ **Clear filter** option to reset and show all products
- ✅ **URL parameter** support (`?category=Chandeliers`)

### Required: Sort by Price
**Requirement**: Allow sorting products by price.

**Implementation**:
- ✅ **Sort dropdown** with "Price: Low to High" and "Price: High to Low" options
- ✅ **Database-level sorting** for performance
- ✅ **Persistent sort** maintained with filters

### Required: Delete Product
**Requirement**: Allow users to delete a product by clicking an "X" in the Actions column.

**Implementation**:
- ✅ **Actions column** with red "Delete" button for each product
- ✅ **Immediate deletion** with database removal
- ✅ **Activity logging** of all deletions

### Bonus: Activity Log
**Requirement**: As a technical reviewer, show a log of all submitted entries.

**Implementation**:
- ✅ **Logs page** at `/logs` showing all product additions and deletions
- ✅ **Timestamp tracking** for each action
- ✅ **Action type** display (Added/Deleted)
- ✅ **Database-backed** log persistence

---

## 🌟 Beyond Requirements - Production Enhancements

### PostgreSQL Database (vs. File Storage)
**Why PostgreSQL?**
- **Permanent data storage** - Products persist even when app restarts
- **Industry standard** - Same database LNY uses in production
- **Performance** - Database indexes on category, price, and created_at for fast queries
- **Data integrity** - Transaction support with automatic rollback on errors
- **Professional skill** - Demonstrates SQLAlchemy ORM and database optimization

**What it achieves:**
- Multi-user concurrent access (file storage would cause conflicts)
- Complex queries and aggregations (category statistics, price averages)
- Database migrations for schema versioning (Flask-Migrate)
- Scalability for thousands of products

### REST API Endpoints
**What the API adds:**
Beyond the web interface, I built 7 REST API endpoints for programmatic access:

```
GET    /api/products           - List all products (with filters)
GET    /api/products/<id>      - Get single product
POST   /api/products           - Create product (requires API key)
PUT    /api/products/<id>      - Update product (requires API key)
DELETE /api/products/<id>      - Delete product (requires API key)
GET    /api/export/products    - Export as CSV/JSON (ETL capability)
GET    /api/stats              - Analytics & statistics
```

**Why this matters for LNY:**
- **System integration** - External platforms can interact with the app
- **ETL pipelines** - Export data for integration with other systems (like LNY backoffice)
- **Mobile apps** - API-first design enables mobile development
- **Automation** - Bulk operations and scheduled tasks

### FastAPI Integration
**What is FastAPI?**
- Modern Python framework for building APIs (alternative to Flask)
- **Automatic documentation** at `/docs` - interactive API testing in browser
- **Type safety** with Python type hints
- Runs alongside Flask on port 8000

**Why I added it:**
- Demonstrates knowledge of **both Flask and FastAPI** (LNY job requirement)
- Learn by comparison - see the same endpoints in two frameworks
- **Interactive docs** at http://localhost:8000/docs to test API calls

### Security Features
**Production-grade security implemented:**

1. **Environment Variables** - Secrets in `.env` file (not in code)
2. **API Authentication** - API key requirement for write operations
3. **Rate Limiting** - 30 req/min for reads, 10 req/min for writes
4. **Input Sanitization** - XSS protection with MarkupSafe
5. **CSRF Protection** - Flask-WTF tokens for web forms
6. **Error Handling** - Custom 404/500 pages, graceful degradation

### Visual Improvements
**Professional UI design:**
- **Navy blue gradient** theme (matching professional standards)
- **Responsive design** - works on mobile, tablet, desktop
- **Modern CSS** - Clean cards, hover effects, smooth transitions
- **User experience** - Clear navigation, intuitive forms, helpful error messages
- **Category dropdown** - Eliminates typos (Chandeliers, Pendant Lights, LED Lights, etc.)

### Testing & Quality Assurance
**Comprehensive test suite:**
- 15+ unit tests with pytest
- API endpoint testing
- Validation and error handling tests
- Authentication tests
- Export functionality tests

Run tests: `pytest tests/ -v`

### Docker Deployment
**One-command setup:**
```bash
docker-compose up
```

Automatically configures:
- PostgreSQL database
- Python dependencies
- Application startup
- Environment configuration

---

## 📚 API Documentation

### Authentication
Protected endpoints require API key in header:
```bash
curl -H "X-API-Key: lny-api-key-12345" http://localhost:5000/api/products
```

### Examples

**Create Product:**
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -H "X-API-Key: lny-api-key-12345" \
  -d '{"name": "Crystal Chandelier", "price": 299.99, "category": "Chandeliers"}'
```

**Export to CSV:**
```bash
curl "http://localhost:5000/api/export/products?format=csv&category=Chandeliers" -o products.csv
```

**Get Statistics:**
```bash
curl http://localhost:5000/api/stats
```

Full API documentation available at: http://localhost:5000/api-docs

---

## 🔒 Security Features

### 1. Environment Variables
- All secrets in `.env` file (never committed to git)
- Database credentials secure
- Different configs for dev/staging/prod

### 2. API Authentication
- API keys required for write operations
- Header-based: `X-API-Key`
- Prevents unauthorized data modification

### 3. Rate Limiting
- 30 requests/minute for GET
- 10 requests/minute for POST/PUT/DELETE
- Prevents abuse and DOS attacks

### 4. Input Sanitization
- XSS protection with MarkupSafe
- HTML escaping on all inputs
- Data validation before database insertion

### 5. CSRF Protection
- Flask-WTF tokens for web forms
- Prevents cross-site request forgery

### 6. Error Handling
- Custom 404/500 error pages
- Database rollback on failures
- Detailed logging for debugging

---

## 🎓 Skills Demonstrated

### Core Python Skills ✅
- Clean, maintainable code
- Object-oriented design (SQLAlchemy models)
- Decorators (authentication, logging)
- Environment-based configuration
- Type validation and sanitization

### Flask Framework ✅
- Application routing
- REST API development
- Template rendering (Jinja2)
- Request/response handling
- Blueprint-ready architecture

### Database Skills ✅
- PostgreSQL integration
- SQLAlchemy ORM
- Database migrations (Flask-Migrate)
- Query optimization with indexes
- Aggregation queries (GROUP BY, COUNT, AVG)
- Transaction management

### API Development ✅
- RESTful endpoint design
- HTTP methods and status codes
- JSON handling
- API authentication
- Rate limiting
- Documentation

### Security ✅
- Secure configuration management
- API key authentication
- XSS prevention
- CSRF protection
- Error handling

### ETL/Integration ✅
- Data export (CSV/JSON)
- Filtering and transformation
- Performance optimization
- Similar to LNY's backoffice integration work

### Testing ✅
- Unit tests with pytest
- Test fixtures
- API testing
- Coverage reporting

### DevOps ✅
- Docker containerization
- Docker Compose
- Database migrations
- Production logging

---

## 📝 License & Submission

- **Candidate**: Louis Sader
- **Position**: Junior Python & ColdFusion Developer
- **Company**: Lighting New York
- **Submitted**: October 2025
- **Repository**: Private GitHub repository shared with `pcollin-lny`

---

## 🙏 Thank You

Thank you again for this opportunity to demonstrate my skills. This project showcases not just the ability to meet requirements, but the drive to build production-ready applications with professional best practices. I'm excited about the possibility of bringing these skills to the Lighting New York team and contributing to your technology initiatives.

I look forward to discussing this project and how my approach aligns with LNY's development standards!

**Ready for production at Lighting New York!** 🚀
