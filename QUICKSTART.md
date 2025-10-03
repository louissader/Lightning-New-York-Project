# Quick Start Guide

## ✅ Setup Complete!

Your PostgreSQL database is set up and ready to use.

### What was done:

1. ✅ PostgreSQL 15 installed and running
2. ✅ Database `lny_products` created
3. ✅ Tables `products` and `logs` created
4. ✅ Python dependencies installed
5. ✅ Database connection configured

### Database Info:

- **Database Name**: `lny_products`
- **Owner**: `louissader`
- **Connection**: `postgresql://louissader@localhost:5432/lny_products`

### Tables Created:

**products** table:
- id (Primary Key)
- name (VARCHAR 200)
- price (NUMERIC 10,2)
- category (VARCHAR 100)
- created_at (TIMESTAMP)

**logs** table:
- id (Primary Key)
- action (VARCHAR 50)
- product_name (VARCHAR 200)
- product_price (NUMERIC 10,2)
- product_category (VARCHAR 100)
- timestamp (TIMESTAMP)

---

## 🚀 Running the Application

### Option 1: Using the run script (easiest)

```bash
./run.sh
```

### Option 2: Manual start

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Add PostgreSQL to PATH
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"

# 3. Run the app
python app.py
```

### Access the Application

Once running, open your browser to:
- **http://localhost:5000**

---

## 🛠️ Useful Commands

### PostgreSQL Commands

```bash
# Add PostgreSQL to PATH (run in every new terminal)
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"

# Check PostgreSQL status
brew services list | grep postgresql

# Start PostgreSQL
brew services start postgresql@15

# Stop PostgreSQL
brew services stop postgresql@15

# Restart PostgreSQL
brew services restart postgresql@15

# Connect to database
psql lny_products

# List all databases
psql postgres -c "\l"

# View tables
psql lny_products -c "\dt"

# View products
psql lny_products -c "SELECT * FROM products;"

# View logs
psql lny_products -c "SELECT * FROM logs;"
```

### Application Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Initialize database (if needed)
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

---

## 🧪 Test the Application

1. **Start the app**: `./run.sh`
2. **Add a product**:
   - Go to http://localhost:5000/add
   - Enter: Name="Test Lamp", Price="99.99", Category="Lighting"
   - Click "Add Product"

3. **View products**:
   - Go to http://localhost:5000
   - You should see your product

4. **Test filtering**:
   - Add more products in different categories
   - Use the "Filter by Category" dropdown

5. **Test sorting**:
   - Add products with different prices
   - Use "Sort by Price" options

6. **Test delete**:
   - Click the "✕ Delete" button
   - Confirm deletion

7. **View logs**:
   - Go to http://localhost:5000/logs
   - See all your actions

---

## 📊 Database Management

### View all products in terminal:

```bash
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
psql lny_products -c "SELECT id, name, price, category, created_at FROM products;"
```

### View all logs in terminal:

```bash
psql lny_products -c "SELECT action, product_name, product_price, timestamp FROM logs;"
```

### Clear all data (start fresh):

```bash
psql lny_products -c "DELETE FROM products;"
psql lny_products -c "DELETE FROM logs;"
```

---

## 🐛 Troubleshooting

### App won't start?

1. Check PostgreSQL is running:
   ```bash
   brew services list | grep postgresql
   ```

2. If not started:
   ```bash
   brew services start postgresql@15
   ```

### Can't connect to database?

1. Verify database exists:
   ```bash
   export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
   psql postgres -c "\l" | grep lny_products
   ```

2. If missing, recreate:
   ```bash
   psql postgres -c "CREATE DATABASE lny_products;"
   ```

### Tables don't exist?

```bash
source .venv/bin/activate
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Tables created!')"
```

---

## 📝 Making PostgreSQL PATH Permanent (Optional)

To avoid typing `export PATH=...` every time, add to your shell profile:

```bash
echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## ✨ Ready for Demo!

Your application is fully functional and ready to demonstrate all features:

- ✅ Add products with name, price, category
- ✅ View products in table format
- ✅ Filter by category
- ✅ Sort by price
- ✅ Delete products
- ✅ View activity logs
- ✅ Professional UI design
- ✅ PostgreSQL database backend

Good luck with your interview! 🎉
