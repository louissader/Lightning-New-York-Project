"""
Unit tests for REST API endpoints.

Run with: python -m pytest tests/ -v
or: python -m unittest discover tests/
"""

import unittest
import json
import os
from app import app, db, Product, Log


class APITestCase(unittest.TestCase):
    """Test case for API endpoints."""

    def setUp(self):
        """Set up test client and database before each test."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory test database
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        self.api_key = os.getenv('API_KEY', 'lny-api-key-12345')

        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_products_empty(self):
        """Test getting products when database is empty."""
        response = self.client.get('/api/products')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['data']), 0)

    def test_create_product(self):
        """Test creating a new product via API."""
        response = self.client.post('/api/products',
            json={'name': 'Test Lamp', 'price': 29.99, 'category': 'Lighting'},
            headers={'X-API-Key': self.api_key})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['name'], 'Test Lamp')
        self.assertEqual(float(data['data']['price']), 29.99)
        self.assertEqual(data['data']['category'], 'Lighting')

    def test_create_product_without_api_key(self):
        """Test that creating product fails without API key."""
        response = self.client.post('/api/products',
            json={'name': 'Test Lamp', 'price': 29.99, 'category': 'Lighting'})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])

    def test_create_product_invalid_data(self):
        """Test validation of invalid product data."""
        response = self.client.post('/api/products',
            json={'name': '', 'price': -10, 'category': ''},
            headers={'X-API-Key': self.api_key})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('errors', data)
        self.assertGreater(len(data['errors']), 0)

    def test_create_product_missing_fields(self):
        """Test that missing required fields are rejected."""
        response = self.client.post('/api/products',
            json={'name': 'Test Lamp'},
            headers={'X-API-Key': self.api_key})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_get_single_product(self):
        """Test retrieving a single product by ID."""
        # First create a product
        with app.app_context():
            product = Product(name='Test Lamp', price=29.99, category='Lighting')
            db.session.add(product)
            db.session.commit()
            product_id = product.id

        # Now get it
        response = self.client.get(f'/api/products/{product_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['name'], 'Test Lamp')

    def test_get_nonexistent_product(self):
        """Test getting a product that doesn't exist."""
        response = self.client.get('/api/products/999')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_update_product(self):
        """Test updating a product."""
        # Create product
        with app.app_context():
            product = Product(name='Old Name', price=10.00, category='Old Category')
            db.session.add(product)
            db.session.commit()
            product_id = product.id

        # Update it
        response = self.client.put(f'/api/products/{product_id}',
            json={'name': 'New Name', 'price': 20.00, 'category': 'New Category'},
            headers={'X-API-Key': self.api_key})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['name'], 'New Name')
        self.assertEqual(float(data['data']['price']), 20.00)

    def test_delete_product(self):
        """Test deleting a product."""
        # Create product
        with app.app_context():
            product = Product(name='To Delete', price=10.00, category='Test')
            db.session.add(product)
            db.session.commit()
            product_id = product.id

        # Delete it
        response = self.client.delete(f'/api/products/{product_id}',
            headers={'X-API-Key': self.api_key})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

        # Verify it's gone
        response = self.client.get(f'/api/products/{product_id}')
        self.assertEqual(response.status_code, 404)

    def test_filter_products_by_category(self):
        """Test filtering products by category."""
        # Create products in different categories
        with app.app_context():
            db.session.add(Product(name='Lamp', price=10.00, category='Lighting'))
            db.session.add(Product(name='Chair', price=50.00, category='Furniture'))
            db.session.add(Product(name='Bulb', price=5.00, category='Lighting'))
            db.session.commit()

        # Filter by Lighting
        response = self.client.get('/api/products?category=Lighting')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['count'], 2)
        for product in data['data']:
            self.assertEqual(product['category'], 'Lighting')

    def test_sort_products_by_price(self):
        """Test sorting products by price."""
        # Create products with different prices
        with app.app_context():
            db.session.add(Product(name='Expensive', price=100.00, category='Test'))
            db.session.add(Product(name='Cheap', price=10.00, category='Test'))
            db.session.add(Product(name='Medium', price=50.00, category='Test'))
            db.session.commit()

        # Sort ascending
        response = self.client.get('/api/products?sort=price_asc')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(float(data['data'][0]['price']), 10.00)
        self.assertEqual(float(data['data'][-1]['price']), 100.00)

        # Sort descending
        response = self.client.get('/api/products?sort=price_desc')
        data = json.loads(response.data)

        self.assertEqual(float(data['data'][0]['price']), 100.00)
        self.assertEqual(float(data['data'][-1]['price']), 10.00)

    def test_export_products_json(self):
        """Test exporting products as JSON."""
        # Create products
        with app.app_context():
            db.session.add(Product(name='Product 1', price=10.00, category='Test'))
            db.session.add(Product(name='Product 2', price=20.00, category='Test'))
            db.session.commit()

        response = self.client.get('/api/export/products?format=json')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 2)
        self.assertIn('exported_at', data)

    def test_export_products_csv(self):
        """Test exporting products as CSV."""
        # Create products
        with app.app_context():
            db.session.add(Product(name='Product 1', price=10.00, category='Test'))
            db.session.commit()

        response = self.client.get('/api/export/products?format=csv')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/csv; charset=utf-8')
        self.assertIn(b'Product 1', response.data)

    def test_get_stats(self):
        """Test getting statistics."""
        # Create products
        with app.app_context():
            db.session.add(Product(name='Lamp 1', price=10.00, category='Lighting'))
            db.session.add(Product(name='Lamp 2', price=20.00, category='Lighting'))
            db.session.add(Product(name='Chair', price=100.00, category='Furniture'))
            db.session.commit()

        response = self.client.get('/api/stats')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['total_products'], 3)
        self.assertEqual(len(data['data']['categories']), 2)


if __name__ == '__main__':
    unittest.main()
