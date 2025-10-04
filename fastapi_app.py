"""
FastAPI Application - Simple Introduction
==========================================

This is a SIMPLE FastAPI app that runs ALONGSIDE your Flask app.

WHY FASTAPI?
- Automatically generates interactive API documentation
- Built for speed (async support)
- Type checking with Python type hints
- Modern alternative to Flask for APIs

HOW IT WORKS WITH YOUR FLASK APP:
- Flask runs on port 5000 (web interface + API)
- FastAPI runs on port 8000 (just API)
- They share the same PostgreSQL database
- You can use either one!

WHAT'S DIFFERENT FROM FLASK?
┌─────────────────┬──────────────────────────┬──────────────────────────┐
│                 │ Flask                    │ FastAPI                  │
├─────────────────┼──────────────────────────┼──────────────────────────┤
│ Purpose         │ Web apps + APIs          │ APIs only                │
│ Documentation   │ Manual                   │ Automatic (Swagger UI)   │
│ Type Checking   │ No                       │ Yes (Pydantic models)    │
│ Async Support   │ Limited                  │ Built-in                 │
│ Speed           │ Good                     │ Very Fast                │
└─────────────────┴──────────────────────────┴──────────────────────────┘
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="LNY Product API (FastAPI Version)",
    description="A simple FastAPI example for managing Lighting New York products",
    version="1.0.0"
)

# Database setup (same database as Flask app!)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://louissader@localhost:5432/lny_products')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Database Model (same as Flask's Product model)
class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Models (for request/response validation)
# This is FastAPI's way of defining data structures
class ProductCreate(BaseModel):
    """Model for creating a new product"""
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    category: str = Field(..., min_length=1, max_length=100, description="Product category")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Crystal Chandelier",
                "price": 499.99,
                "category": "Chandeliers"
            }
        }

class ProductResponse(BaseModel):
    """Model for product response"""
    id: int
    name: str
    price: float
    category: str
    created_at: datetime

    class Config:
        from_attributes = True

# API ENDPOINTS
# ==============

@app.get("/")
async def root():
    """
    Welcome endpoint - explains what FastAPI is
    """
    return {
        "message": "Welcome to the FastAPI version of LNY Product API!",
        "what_is_fastapi": "FastAPI is a modern, fast framework for building APIs",
        "why_use_it": "Automatic docs, type safety, and high performance",
        "docs_url": "Visit /docs for interactive API documentation",
        "flask_app": "Your Flask app is still running on port 5000",
        "this_api": "This FastAPI is running on port 8000"
    }

@app.get("/products", response_model=List[ProductResponse])
async def get_products(category: Optional[str] = None):
    """
    Get all products (optionally filter by category)

    This is similar to Flask's /api/products endpoint but:
    - Automatically validates the response matches ProductResponse model
    - Shows up in interactive docs at /docs
    - Type hints make it clear what data is expected
    """
    db = SessionLocal()
    try:
        query = db.query(Product)

        # Filter by category if provided
        if category:
            query = query.filter(Product.category == category)

        products = query.all()
        return products
    finally:
        db.close()

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """
    Get a single product by ID

    FastAPI automatically:
    - Converts product_id to an integer
    - Returns 422 error if product_id is not a number
    - Validates the response
    """
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

        return product
    finally:
        db.close()

@app.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate):
    """
    Create a new product

    FastAPI automatically:
    - Validates the request body matches ProductCreate model
    - Returns 422 error if validation fails (e.g., price is negative)
    - Documents the expected request format
    """
    db = SessionLocal()
    try:
        # Create new product
        new_product = Product(
            name=product.name,
            price=product.price,
            category=product.category
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product
    finally:
        db.close()

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    """
    Delete a product by ID
    """
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

        db.delete(product)
        db.commit()

        return {"success": True, "message": f"Product {product_id} deleted"}
    finally:
        db.close()

@app.get("/compare-to-flask")
async def compare():
    """
    Endpoint that explains the differences between Flask and FastAPI
    """
    return {
        "comparison": {
            "Flask": {
                "what_you_built": "A web application with HTML pages AND API endpoints",
                "port": 5000,
                "best_for": "Full web applications with forms, templates, and user interface",
                "your_routes": ["/", "/add", "/delete", "/api/products", "/export"],
                "authentication": "API key via @require_api_key decorator",
                "documentation": "Manual (you wrote it in README)"
            },
            "FastAPI": {
                "what_this_is": "API-only, no HTML pages",
                "port": 8000,
                "best_for": "Building pure APIs for mobile apps, microservices, etc.",
                "your_routes": ["/products", "/products/{id}"],
                "authentication": "Can add OAuth2, JWT, etc.",
                "documentation": "Automatic at /docs (try it!)"
            }
        },
        "when_to_use_what": {
            "use_flask": "When you need web pages + API (like your current app)",
            "use_fastapi": "When you only need an API (mobile backend, microservices)",
            "use_both": "When you want the best of both worlds (what you're doing now!)"
        },
        "try_it": "Visit http://localhost:8000/docs to see FastAPI's automatic documentation!"
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 Starting FastAPI Server")
    print("="*60)
    print("📍 API running at: http://localhost:8000")
    print("📚 Interactive docs: http://localhost:8000/docs")
    print("📖 Alternative docs: http://localhost:8000/redoc")
    print("\n💡 TIP: Your Flask app is still running on port 5000")
    print("   - Flask = Web interface + API (port 5000)")
    print("   - FastAPI = API only (port 8000)")
    print("\n🔍 Try these endpoints:")
    print("   - GET  http://localhost:8000/products")
    print("   - GET  http://localhost:8000/compare-to-flask")
    print("   - POST http://localhost:8000/products")
    print("\nPress Ctrl+C to stop")
    print("="*60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
