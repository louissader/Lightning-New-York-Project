# Product Management System - LNY Interview Project

> **A Flask-based product management application demonstrating skills required for the Junior Python Developer role at Lighting New York**

---

## 🎯 Project Overview

This project demonstrates my ability to build production-ready Python applications with Flask, PostgreSQL, and REST APIs - directly aligned with the technical requirements for the Junior Python & ColdFusion Developer position at Lighting New York.

### Why This Project Matters for LNY

At LNY, I would be working on:
- **Python applications and APIs** using Flask and FastAPI ✅
- **PostgreSQL database** operations and optimization ✅
- **ETL pipelines** moving data between systems ✅
- **REST APIs with JSON** handling ✅
- **Clean, documented code** ready for code reviews ✅

This project showcases all of these skills in action.

---

## 🔧 Technical Stack (Matching LNY Requirements)

| Requirement | Implementation | LNY Application |
|------------|----------------|-----------------|
| **Flask/FastAPI** | Flask with REST API endpoints | Similar to LNY's Python API development |
| **PostgreSQL** | Full PostgreSQL integration with SQLAlchemy | Same database LNY uses |
| **REST APIs** | Complete CRUD API with JSON responses | Building APIs to integrate LNY systems |
| **ETL/Data Export** | CSV/JSON export functionality | Like moving data between LNY backoffice and other platforms |
| **Error Handling** | Comprehensive validation & logging | Production-ready error handling |
| **Documentation** | API docs similar to Swagger | Documentation skills for Confluence |
| **Database Queries** | Optimized queries with aggregations | Working with MSSQL/PostgreSQL at LNY |

---

## ✨ Key Features (Aligned with Job Description)

### 1. **REST API Development** (Flask Requirement)
- **7 RESTful endpoints** with proper HTTP methods
- JSON request/response handling
- Input validation and error handling
- Similar to building APIs at LNY for system integrations

**API Endpoints:**
- `GET /api/products` - List all products with filtering/sorting
- `GET /api/products/<id>` - Get single product
- `POST /api/products` - Create new product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product
- `GET /api/export/products` - Export data (ETL)
- `GET /api/stats` - Database statistics

### 2. **PostgreSQL Database Integration**
- SQLAlchemy ORM for clean database operations
- Proper schema design with relationships
- Query optimization and aggregations
- Transaction management with rollback

**Tables:**
- `products` - Main product data
- `logs` - Activity tracking for audit trails

### 3. **ETL/Data Pipeline Capabilities**
- **Export to CSV** - Extract data for external systems
- **Export to JSON** - API-based data transfer
- **Filtering options** - Category-based data extraction
- Demonstrates ability to move data between systems (like LNY backoffice to other platforms)

### 4. **Clean, Maintainable Code**
- Well-documented functions with docstrings
- Modular code structure
- Proper error handling and logging
- Ready for code reviews and team collaboration

### 5. **Production-Ready Features**
- Comprehensive logging system (app.log)
- Data validation on all inputs
- Error handling with appropriate HTTP status codes
- Database connection management

---

## 📊 How This Relates to LNY Work

### **Scenario 1: Building APIs for System Integration**
*At LNY: "Develop Python APIs using Flask to connect backoffice system to external platforms"*

**In this project:**
- Built 7 REST API endpoints (app.py:196-577)
- Proper HTTP methods (GET, POST, PUT, DELETE)
- JSON request/response handling
- Input validation and error responses

### **Scenario 2: ETL Data Pipelines**
*At LNY: "Build ETLs that move data between ColdFusion backoffice and other systems"*

**In this project:**
- Export endpoint extracts data in CSV/JSON (app.py:449-522)
- Filtering and transformation of data
- Similar to extracting product data from one system to another

### **Scenario 3: PostgreSQL Database Work**
*At LNY: "Work with PostgreSQL for queries, schema changes, and optimization"*

**In this project:**
- Full PostgreSQL integration with SQLAlchemy ORM
- Optimized queries with filtering and sorting
- Aggregation queries (COUNT, AVG, SUM) in stats endpoint (app.py:538-543)
- Proper indexing with primary keys

### **Scenario 4: Documentation**
*At LNY: "Document workflows using tools like Confluence and Swagger"*

**In this project:**
- Complete API documentation page (/api-docs)
- Similar to Swagger/OpenAPI documentation
- Code comments and docstrings throughout
- README with setup instructions

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL 15
- Homebrew (macOS)

### Quick Setup

1. **Clone the repository**
```bash
cd lnyProject
```

2. **Start PostgreSQL** (already configured)
```bash
brew services start postgresql@15
```

3. **Install dependencies**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

4. **Run the application**
```bash
./run.sh
```

5. **Access the application**
- Web UI: http://localhost:5000
- API Docs: http://localhost:5000/api-docs

### Database Configuration
- **Database**: `lny_products`
- **Connection**: `postgresql://louissader@localhost:5432/lny_products`
- Tables auto-created on first run

---

## 📚 API Documentation

Visit [http://localhost:5000/api-docs](http://localhost:5000/api-docs) for complete API documentation.

### Quick API Examples

**Get all products:**
```bash
curl http://localhost:5000/api/products
```

**Create a product:**
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "LED Lamp", "price": 49.99, "category": "Lighting"}'
```

**Export to CSV (ETL):**
```bash
curl http://localhost:5000/api/export/products?format=csv -o products.csv
```

**Get statistics:**
```bash
curl http://localhost:5000/api/stats
```

---

## 🎓 Skills Demonstrated

### Python Development ✅
- Clean, maintainable Python code
- Object-oriented design with SQLAlchemy models
- Proper error handling and logging
- Type validation and data sanitization

### Flask Framework ✅
- Application structure and routing
- Request/response handling
- Template rendering with Jinja2
- REST API development

### Database Skills ✅
- PostgreSQL integration
- SQLAlchemy ORM
- Query optimization
- Database schema design
- Aggregation queries (GROUP BY, COUNT, AVG, SUM)

### API Development ✅
- RESTful endpoint design
- HTTP methods and status codes
- JSON data handling
- API documentation

### ETL/Integration ✅
- Data export functionality
- CSV and JSON formats
- Data filtering and transformation
- Similar to LNY's data pipeline work

### Documentation ✅
- Code comments and docstrings
- API documentation
- README with clear instructions
- Ready for knowledge sharing

---

## 📁 Project Structure

```
lnyProject/
├── app.py                  # Main Flask application with API endpoints
├── requirements.txt        # Python dependencies
├── run.sh                  # Easy startup script
├── README.md              # This file
├── QUICKSTART.md          # Setup guide
├── .gitignore             # Git ignore rules
├── static/
│   └── style.css          # Modern, responsive CSS
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Product listing with filters
    ├── add_product.html   # Add product form
    ├── logs.html          # Activity logs
    └── api_docs.html      # API documentation
```

---

## ��� Code Quality Highlights

### Well-Documented Functions
Every function includes clear docstrings explaining purpose and usage:
```python
def validate_product_data(data):
    """Validate product data for API requests."""
    # Comprehensive validation logic
```

### Proper Error Handling
All API endpoints include try-catch blocks with appropriate error responses:
```python
except Exception as e:
    logger.error(f"API Error: {str(e)}")
    return jsonify({'success': False, 'error': 'Error message'}), 500
```

### Logging System
Production-ready logging to track all operations:
```python
logger.info(f"API: Created product {new_product.id}")
```

### Input Validation
Comprehensive validation preventing bad data:
```python
errors = validate_product_data(data)
if errors:
    return jsonify({'success': False, 'errors': errors}), 400
```

---

## 🎯 Interview Talking Points

### Question: "Tell me about a Python project you've built"

**Answer**: "I built a product management system using Flask and PostgreSQL that demonstrates the exact skills needed at LNY:

1. **REST APIs with Flask** - I created 7 RESTful endpoints with proper HTTP methods, JSON handling, and error responses - similar to what I'd build at LNY to integrate the backoffice with external systems.

2. **PostgreSQL Integration** - Used SQLAlchemy ORM for database operations, wrote optimized queries with aggregations, and designed a proper schema - the same skills needed for working with LNY's databases.

3. **ETL Functionality** - Built data export endpoints that can extract products as CSV or JSON with filtering - demonstrating the data pipeline work I'd do moving data between LNY systems.

4. **Production Quality** - Implemented comprehensive logging, error handling, input validation, and API documentation - showing I write maintainable code ready for team collaboration."

### Question: "How would you approach learning ColdFusion?"

**Answer**: "Just like I built this Flask application, I'd:
1. Start with the ColdFusion documentation and learn CFML syntax
2. Study existing LNY code to understand patterns and conventions
3. Make small enhancements with senior developer guidance
4. Apply my REST API and database knowledge - the concepts transfer
5. Document what I learn to help future team members"

---

## 🚀 Future Enhancements

Based on LNY's needs, this could be extended with:
- [ ] User authentication and authorization
- [ ] Batch import functionality
- [ ] Advanced filtering and search
- [ ] Integration with external APIs
- [ ] Real-time data synchronization
- [ ] Performance monitoring and metrics

---

## 📞 Questions & Discussion

I'm excited to discuss:
- How this project demonstrates my readiness for the Junior Python Developer role
- How my API development skills would help integrate LNY systems
- How my database experience translates to working with LNY's PostgreSQL/MSSQL
- My approach to learning ColdFusion and contributing to the backoffice system
- How my documentation skills would help with Confluence and team collaboration

---

## 📝 Submission Details

- **Candidate**: Louis Sader
- **Position**: Junior Python & ColdFusion Developer
- **Submitted**: October 2025
- **GitHub**: Private repository shared with pcollin-lny

---

Built with Python, Flask, PostgreSQL - Ready for production at Lighting New York 🚀
