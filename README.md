# LNY Product Management Application

A Flask-based product management system with PostgreSQL database, built for the Lighting New York Junior Developer Interview Exercise.

## Features

- ✅ Add products with name, price, and category
- ✅ View all products in a table format
- ✅ Filter products by category
- ✅ Sort products by price (ascending/descending)
- ✅ Delete products with confirmation
- ✅ Activity logs tracking all additions and deletions
- ✅ Automatic timestamp tracking (Created At)
- ✅ Modern, responsive UI design
- ✅ PostgreSQL database integration

## Technical Stack

- **Backend**: Python 3.x, Flask
- **Database**: PostgreSQL
- **ORM**: Flask-SQLAlchemy
- **Frontend**: HTML5, CSS3, Jinja2 templates

## Prerequisites

Before running the application, ensure you have the following installed:

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **PostgreSQL** - [Download PostgreSQL](https://www.postgresql.org/download/)

## PostgreSQL Database Setup

### Step 1: Install PostgreSQL

**macOS (using Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Windows:**
- Download and install from [PostgreSQL official website](https://www.postgresql.org/download/windows/)
- Follow the installation wizard

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Create Database and User

1. **Access PostgreSQL shell:**
```bash
psql postgres
```

2. **Create a database for the application:**
```sql
CREATE DATABASE lny_products;
```

3. **Create a user (optional but recommended):**
```sql
CREATE USER lny_user WITH PASSWORD 'your_secure_password';
```

4. **Grant privileges:**
```sql
GRANT ALL PRIVILEGES ON DATABASE lny_products TO lny_user;
```

5. **Exit PostgreSQL shell:**
```sql
\q
```

### Step 3: Configure Database Connection

The application uses the following default connection string:
```
postgresql://postgres:password@localhost:5432/lny_products
```

**To customize the connection:**

1. Create a `.env` file in the project root:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/lny_products
```

2. Replace:
   - `username` with your PostgreSQL username (default: `postgres`)
   - `password` with your PostgreSQL password
   - `lny_products` with your database name if different

## Installation and Setup

### Step 1: Clone or Download the Repository

```bash
cd /path/to/lnyProject
```

### Step 2: Create a Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database Tables

The application automatically creates the required database tables on first run. The tables are:

- `products` - Stores product information
- `logs` - Stores activity logs

You can also manually initialize:
```python
python3
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

## Running the Application

1. **Ensure PostgreSQL is running:**
```bash
# macOS (if using Homebrew)
brew services list

# Linux
sudo systemctl status postgresql
```

2. **Start the Flask application:**
```bash
python app.py
```

3. **Access the application:**
   - Open your browser and go to: `http://127.0.0.1:5000`
   - Or: `http://localhost:5000`

## Using the Application

### Adding Products

1. Click **"Add Product"** in the navigation
2. Fill in the form:
   - **Name**: Product name (required)
   - **Price**: Product price in dollars (required)
   - **Category**: Product category (required)
3. Click **"Add Product"** button
4. Product will appear in the listing with automatic timestamp

### Viewing Products

- The home page displays all products in a table
- Shows: Name, Price, Category, Created At, and Actions
- Products are sorted by newest first by default

### Filtering Products

1. Use the **"Filter by Category"** dropdown
2. Select a category
3. Click **"Apply Filters"**
4. Click **"Clear Filters"** to reset

### Sorting Products

1. Use the **"Sort by Price"** dropdown
2. Choose:
   - **Default (Newest First)**
   - **Price: Low to High**
   - **Price: High to Low**
3. Click **"Apply Filters"**

### Deleting Products

1. Click the **"✕ Delete"** button in the Actions column
2. Confirm the deletion in the popup
3. Product is removed and logged

### Viewing Logs

1. Click **"Logs"** in the navigation
2. View all additions (green) and deletions (red)
3. See timestamp of each action

## Database Schema

### Products Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Logs Table
```sql
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    action VARCHAR(50) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    product_price NUMERIC(10, 2),
    product_category VARCHAR(100),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## Troubleshooting

### PostgreSQL Connection Issues

**Error: `connection refused`**
- Ensure PostgreSQL is running: `brew services list` or `sudo systemctl status postgresql`
- Start if stopped: `brew services start postgresql@15` or `sudo systemctl start postgresql`

**Error: `password authentication failed`**
- Check your password in the connection string
- Reset PostgreSQL password if needed:
```bash
psql postgres
\password postgres
```

**Error: `database does not exist`**
- Create the database: `createdb lny_products`
- Or use psql: `CREATE DATABASE lny_products;`

### Python/Flask Issues

**Error: `ModuleNotFoundError`**
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

**Error: `No module named 'psycopg2'`**
- Install psycopg2-binary: `pip install psycopg2-binary`

## Development Notes

### Design Decisions

1. **PostgreSQL** - Chosen to match company technology stack
2. **Flask-SQLAlchemy** - Provides clean ORM interface and database abstraction
3. **Price as Numeric** - Ensures accurate decimal handling for currency
4. **Activity Logs** - Implemented as bonus feature for audit trail
5. **Responsive Design** - Mobile-friendly CSS for better usability

### Future Enhancements

- User authentication
- Edit product functionality
- Bulk operations
- CSV export
- Search functionality
- Pagination for large datasets

## Project Structure

```
lnyProject/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── static/
│   └── style.css          # CSS styling
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Product listing page
    ├── add_product.html   # Add product form
    └── logs.html          # Activity logs page
```

## Submission

- **Repository**: Private GitHub repository
- **Shared with**: pcollin-lny
- **Due**: 10/8/2025 at 12 pm EST

## Contact

For questions about this exercise, please contact Heidi at Lighting New York.
