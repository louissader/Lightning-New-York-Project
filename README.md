# Product Management System - LNY Interview Project

> **A production-ready Flask application demonstrating professional Python development skills for the Junior Python Developer role at Lighting New York**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## 🎯 Project Overview

This project demonstrates my ability to build **production-ready Python applications** with Flask, PostgreSQL, and REST APIs - directly aligned with the technical requirements for the Junior Python & ColdFusion Developer position at Lighting New York.

### Why This Project Matters for LNY

At LNY, I would be working on:
- **Python applications and APIs** using Flask and FastAPI ✅
- **PostgreSQL database** operations and optimization ✅
- **ETL pipelines** moving data between systems ✅
- **REST APIs with JSON** handling ✅
- **Clean, documented code** ready for code reviews ✅
- **Security best practices** and production deployment ✅

This project showcases all of these skills in a real-world application.

---

## 🔧 Technical Stack (Matching LNY Requirements)

| Requirement | Implementation | LNY Application |
|------------|----------------|-----------------|
| **Flask/FastAPI** | Flask with 7 REST API endpoints | Similar to LNY's Python API development |
| **PostgreSQL** | Full integration with SQLAlchemy ORM | Same database LNY uses |
| **REST APIs** | Complete CRUD API with JSON responses | Building APIs to integrate LNY systems |
| **ETL/Data Export** | CSV/JSON export functionality | Like moving data between LNY backoffice and platforms |
| **Error Handling** | Comprehensive validation & logging | Production-ready error handling |
| **Documentation** | API docs similar to Swagger | Documentation skills for Confluence |
| **Database Optimization** | Indexed queries with aggregations | Working with MSSQL/PostgreSQL at LNY |
| **Security** | API keys, rate limiting, input sanitization | Production security standards |
| **Testing** | Unit tests with pytest | Code quality assurance |
| **Containerization** | Docker & Docker Compose | Modern deployment practices |

---

## ✨ Key Features (Aligned with Job Description)

### 1. **REST API Development** (Flask Requirement)
- **7 RESTful endpoints** with proper HTTP methods (GET, POST, PUT, DELETE)
- JSON request/response handling
- Input validation and comprehensive error handling
- API key authentication for write operations
- Rate limiting to prevent abuse (30 req/min for reads, 10 req/min for writes)
- Similar to building APIs at LNY for system integrations

**API Endpoints:**
```
GET    /api/products           - List products (filter & sort)
GET    /api/products/<id>      - Get single product
POST   /api/products           - Create product (requires API key)
PUT    /api/products/<id>      - Update product (requires API key)
DELETE /api/products/<id>      - Delete product (requires API key)
GET    /api/export/products    - Export data as CSV/JSON (ETL)
GET    /api/stats              - Database statistics & analytics
```

### 2. **PostgreSQL Database Integration**
- SQLAlchemy ORM for clean database operations
- **Database indexes** on category, price, created_at for query optimization
- Query optimization with aggregations (GROUP BY, COUNT, AVG, SUM)
- Transaction management with automatic rollback on errors
- Flask-Migrate for database schema version control

**Tables:**
- `products` - Product data with indexed columns
- `logs` - Activity tracking for audit trails

### 3. **ETL/Data Pipeline Capabilities**
- **Export to CSV** - Extract data for Excel, data warehouses, external systems
- **Export to JSON** - API-based data transfer
- **Filtering options** - Category-based data extraction
- Demonstrates ability to move data between systems (like LNY backoffice to other platforms)

### 4. **Security & Production Features**
- **Environment Variables** - Secure configuration via `.env` files
- **API Authentication** - API key requirement for write operations
- **Rate Limiting** - Prevent API abuse (Flask-Limiter)
- **Input Sanitization** - XSS protection with MarkupSafe
- **CSRF Protection** - Flask-WTF security
- **Error Handling** - Custom 404/500 pages, graceful degradation
- **Logging** - Comprehensive application logging with performance metrics

### 5. **Performance Optimization**
- **Database Indexes** - Fast queries on category, price, date
- **Performance Monitoring** - Execution time logging for slow queries
- **Query Optimization** - Database-level filtering and aggregation
- **Connection Pooling** - Efficient database connection management

### 6. **Testing & Quality Assurance**
- **Unit Tests** - Comprehensive test suite with pytest
- **Test Coverage** - API endpoints, validation, database operations
- **Continuous Testing** - Easy to run: `pytest tests/ -v`

### 7. **DevOps & Deployment**
- **Docker Support** - Containerized application
- **Docker Compose** - One-command setup with PostgreSQL
- **Database Migrations** - Version-controlled schema changes
- **Environment Management** - Development/production configurations

---

## 📊 How This Relates to LNY Work

### **Scenario 1: Building APIs for System Integration**
*At LNY: "Develop Python APIs using Flask to connect backoffice system to external platforms"*

**In this project:**
- Built 7 REST API endpoints ([app.py:321-672](app.py#L321-L672))
- Proper HTTP methods (GET, POST, PUT, DELETE)
- JSON request/response handling
- Input validation and error responses
- API authentication with keys
- Rate limiting for protection

### **Scenario 2: ETL Data Pipelines**
*At LNY: "Build ETLs that move data between ColdFusion backoffice and other systems"*

**In this project:**
- Export endpoint extracts data in CSV/JSON ([app.py:550-617](app.py#L550-L617))
- Filtering and transformation of data
- Similar to extracting product data from one system to another
- Performance monitoring for large datasets

### **Scenario 3: PostgreSQL Database Work**
*At LNY: "Work with PostgreSQL for queries, schema changes, and optimization"*

**In this project:**
- Full PostgreSQL integration with SQLAlchemy ORM
- Database indexes for performance ([app.py:74-78](app.py#L74-L78))
- Aggregation queries (COUNT, AVG, SUM) ([app.py:634-639](app.py#L634-L639))
- Flask-Migrate for schema version control
- Transaction management with rollback

### **Scenario 4: Security & Production Readiness**
*At LNY: "Write clean, maintainable code" and work in production environments*

**In this project:**
- Environment-based configuration (no hardcoded secrets)
- API key authentication
- Rate limiting
- Input sanitization
- Error handling with rollback
- Comprehensive logging

### **Scenario 5: Documentation**
*At LNY: "Document workflows using tools like Confluence and Swagger"*

**In this project:**
- Complete API documentation page ([/api-docs](http://localhost:5000/api-docs))
- Similar to Swagger/OpenAPI documentation
- Code comments and docstrings throughout
- README with setup instructions

---

## 🚀 Getting Started

### Option 1: Docker (Recommended - Fastest Setup)

**Prerequisites:**
- Docker and Docker Compose installed

**Setup:**
```bash
# Clone repository
cd lnyProject

# Start everything with one command
docker-compose up

# Access application
open http://localhost:5000
```

That's it! Docker automatically:
- Sets up PostgreSQL database
- Installs all dependencies
- Creates database tables
- Starts the application

### Option 2: Local Installation

**Prerequisites:**
- Python 3.9+
- PostgreSQL 15
- Virtual environment

**Setup:**

1. **Install PostgreSQL**
```bash
# macOS
brew install postgresql@15
brew services start postgresql@15

# Create database
psql postgres -c "CREATE DATABASE lny_products;"
```

2. **Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# DATABASE_URL=postgresql://your_username@localhost:5432/lny_products
```

3. **Install Dependencies**
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

4. **Initialize Database**
```bash
# Run migrations
flask db upgrade

# Or let app create tables automatically
python app.py
```

5. **Run Application**
```bash
# Using the run script
./run.sh

# Or manually
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
python app.py
```

6. **Access Application**
- Web UI: http://localhost:5000
- API Docs: http://localhost:5000/api-docs

---

## 📚 API Documentation

### Authentication

Protected endpoints (POST, PUT, DELETE) require an API key:
```bash
curl -H "X-API-Key: your-api-key" http://localhost:5000/api/products
```

Set your API key in `.env`:
```
API_KEY=your-secure-api-key-here
```

### API Examples

**Get all products:**
```bash
curl http://localhost:5000/api/products
```

**Create a product:**
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -H "X-API-Key: lny-api-key-12345" \
  -d '{
    "name": "LED Lamp",
    "price": 49.99,
    "category": "Lighting"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Product created successfully",
  "data": {
    "id": 1,
    "name": "LED Lamp",
    "price": 49.99,
    "category": "Lighting",
    "created_at": "2025-10-03T15:00:00"
  }
}
```

**Update a product:**
```bash
curl -X PUT http://localhost:5000/api/products/1 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: lny-api-key-12345" \
  -d '{
    "name": "LED Lamp Pro",
    "price": 59.99,
    "category": "Lighting"
  }'
```

**Export to CSV (ETL):**
```bash
curl http://localhost:5000/api/export/products?format=csv -o products.csv
```

**Export filtered data:**
```bash
curl "http://localhost:5000/api/export/products?format=csv&category=Lighting" -o lighting.csv
```

**Get statistics:**
```bash
curl http://localhost:5000/api/stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_products": 50,
    "categories": [
      {
        "category": "Lighting",
        "count": 25,
        "average_price": 45.50,
        "total_value": 1137.50
      }
    ],
    "recent_activity": [...]
  }
}
```

### Error Responses

**Validation Error (400):**
```json
{
  "success": false,
  "errors": [
    "Product name is required",
    "Price must be a positive number"
  ]
}
```

**Not Found (404):**
```json
{
  "success": false,
  "error": "Product not found"
}
```

**Unauthorized (401):**
```json
{
  "success": false,
  "error": "Invalid or missing API key"
}
```

**Rate Limit (429):**
```json
{
  "success": false,
  "error": "Rate limit exceeded. Please try again later."
}
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test
pytest tests/test_api.py::APITestCase::test_create_product -v
```

**Test Coverage Includes:**
- API endpoint functionality
- Data validation
- Error handling
- Authentication
- Filtering and sorting
- CSV/JSON export
- Database operations

---

## 🗄️ Database Management

### Using Flask-Migrate

```bash
# Initialize migrations (first time only)
flask db init

# Create a migration after model changes
flask db migrate -m "Add new column"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade
```

### Direct PostgreSQL Access

```bash
# Add PostgreSQL to PATH
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"

# Connect to database
psql lny_products

# View tables
\dt

# Query products
SELECT * FROM products;

# View statistics
SELECT category, COUNT(*), AVG(price)
FROM products
GROUP BY category;
```

---

## 🔒 Security Features

### 1. Environment Variables
- All secrets stored in `.env` file (not committed to git)
- Different configurations for dev/staging/prod
- Database credentials never in code

### 2. API Authentication
- API keys required for write operations
- Header-based authentication: `X-API-Key`
- Configurable per environment

### 3. Rate Limiting
- 30 requests/minute for GET endpoints
- 10 requests/minute for POST/PUT/DELETE
- Prevents API abuse and DOS attacks

### 4. Input Sanitization
- XSS protection with MarkupSafe
- HTML escaping on all user inputs
- Validates all data before database insertion

### 5. CSRF Protection
- Flask-WTF CSRF tokens for web forms
- API endpoints exempt (use API keys instead)

### 6. Error Handling
- Graceful error pages (404, 500)
- Database rollback on transaction failures
- Detailed logging for debugging

---

## 📈 Performance Optimizations

### Database Indexes
```python
# Automatically created on:
- category (for filtering)
- price (for sorting)
- created_at (for date queries)
```

### Query Optimization
- Filtering done at database level
- Aggregations use SQL GROUP BY (not Python)
- Efficient pagination support

### Performance Monitoring
```python
# All slow operations are logged
@log_performance decorator tracks execution time

# Example log output:
# api_get_products executed in 0.045s
# api_get_stats executed in 0.123s
```

---

## 🐳 Docker Deployment

### Development
```bash
docker-compose up
```

### Production
```bash
# Build image
docker build -t lny-product-manager .

# Run container
docker run -p 5000:5000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=production-secret \
  -e API_KEY=production-api-key \
  lny-product-manager
```

### Environment Variables (Docker)
Set in `docker-compose.yml` or pass via `-e`:
- `DATABASE_URL`
- `SECRET_KEY`
- `API_KEY`
- `FLASK_ENV`
- `DEBUG`

---

## 📁 Project Structure

```
lnyProject/
├── app.py                      # Main Flask application (680 lines)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── Dockerfile                 # Docker container config
├── docker-compose.yml         # Multi-container setup
├── run.sh                     # Quick start script
├── README.md                  # This file
├── QUICKSTART.md             # Quick setup guide
├── LNY_SKILLS_SHOWCASE.md    # Feature breakdown
│
├── static/
│   └── style.css             # Modern, responsive CSS
│
├── templates/
│   ├── base.html             # Base template
│   ├── index.html            # Product listing with filters
│   ├── add_product.html      # Add product form
│   ├── logs.html             # Activity logs
│   ├── api_docs.html         # API documentation
│   ├── 404.html              # Not found error page
│   └── 500.html              # Server error page
│
├── tests/
│   ├── __init__.py
│   └── test_api.py           # Comprehensive API tests
│
└── migrations/               # Database version control (Flask-Migrate)
    └── versions/
```

---

## 🎓 Skills Demonstrated

### Python Development ✅
- Clean, maintainable Python code
- Object-oriented design with SQLAlchemy models
- Decorators for authentication and logging
- Environment-based configuration
- Type validation and data sanitization

### Flask Framework ✅
- Application structure and routing
- Request/response handling
- Template rendering with Jinja2
- REST API development
- Blueprint-ready architecture

### Database Skills ✅
- PostgreSQL integration
- SQLAlchemy ORM
- Database migrations (Flask-Migrate)
- Query optimization with indexes
- Aggregation queries (GROUP BY, COUNT, AVG, SUM)
- Transaction management

### API Development ✅
- RESTful endpoint design
- HTTP methods and status codes
- JSON data handling
- API authentication
- Rate limiting
- API documentation

### Security ✅
- Environment variable management
- API key authentication
- Input sanitization (XSS prevention)
- CSRF protection
- Rate limiting
- Secure error handling

### ETL/Integration ✅
- Data export functionality
- CSV and JSON formats
- Data filtering and transformation
- Performance optimization for large datasets

### Testing ✅
- Unit tests with pytest
- Test fixtures and teardown
- Mock data and assertions
- Test coverage reporting

### DevOps ✅
- Docker containerization
- Docker Compose orchestration
- Database migrations
- Environment management
- Production-ready logging

### Documentation ✅
- Code comments and docstrings
- API documentation (Swagger-style)
- README with clear instructions
- Setup guides and examples

---

## 🎯 Interview Talking Points

### "Tell me about your Python project"

"I built a production-ready product management system using Flask and PostgreSQL that demonstrates every skill you need at LNY:

1. **REST APIs with Flask** - I created 7 RESTful endpoints with authentication, rate limiting, and comprehensive error handling - exactly what I'd build at LNY to integrate the backoffice with external systems.

2. **PostgreSQL with Optimization** - Used SQLAlchemy ORM with database indexes, aggregation queries, and Flask-Migrate for schema versioning - the same professional database work I'd do at LNY.

3. **ETL Capabilities** - Built export endpoints that extract data from PostgreSQL and transform it to CSV or JSON with filtering - demonstrating the data pipeline work of moving data between LNY systems.

4. **Security & Production Quality** - Implemented API authentication, rate limiting, input sanitization, environment-based config, and comprehensive logging - showing I understand production requirements.

5. **Testing & DevOps** - Added unit tests with pytest, Docker containerization, and database migrations - demonstrating I care about code quality and deployment.

The project goes beyond requirements to show how I'd contribute to a professional development team."

### "How would you approach learning ColdFusion?"

"Just like I built this Flask application, I'd:
1. Study ColdFusion documentation and learn CFML syntax
2. Read existing LNY code to understand patterns and conventions
3. Start with small enhancements under senior developer guidance
4. Apply my REST API and database knowledge - the concepts transfer
5. Document what I learn to help future team members

My experience with Flask, PostgreSQL, and API development gives me a strong foundation to quickly learn ColdFusion."

---

## 🚀 Production Deployment Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to secure random value
- [ ] Change `API_KEY` to secure random value
- [ ] Set `DEBUG=False` in environment
- [ ] Use production PostgreSQL instance
- [ ] Set up SSL/TLS certificates
- [ ] Configure proper CORS if needed
- [ ] Set up application monitoring
- [ ] Configure log rotation
- [ ] Set up database backups
- [ ] Configure firewall rules
- [ ] Review rate limits for production load
- [ ] Set up CI/CD pipeline
- [ ] Configure health check endpoints

---

## 📝 License & Submission

- **Candidate**: Louis Sader
- **Position**: Junior Python & ColdFusion Developer
- **Company**: Lighting New York
- **Submitted**: October 2025
- **Repository**: Private GitHub repository shared with pcollin-lny

---

## 🙏 Acknowledgments

Built with modern web development best practices:
- Flask framework and ecosystem
- PostgreSQL database
- Docker for containerization
- pytest for testing
- Professional security standards

**Ready for production at Lighting New York!** 🚀

---

## 📞 Questions & Support

For questions about this project or the interview process, please contact:
- **Technical Questions**: Review the API documentation at `/api-docs`
- **Setup Issues**: See QUICKSTART.md for troubleshooting
- **Interview Questions**: Contact Heidi at Lighting New York

---

**This project demonstrates production-ready Python development skills perfectly aligned with LNY's Junior Python Developer position requirements.**
