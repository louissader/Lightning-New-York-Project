-- LNY Products Database Setup Script
-- Run this script to set up the PostgreSQL database

-- Create the database
CREATE DATABASE lny_products;

-- Connect to the database
\c lny_products

-- Create a user (optional)
-- Uncomment and modify if you want a dedicated user
-- CREATE USER lny_user WITH PASSWORD 'your_secure_password';
-- GRANT ALL PRIVILEGES ON DATABASE lny_products TO lny_user;

-- The tables will be created automatically by Flask-SQLAlchemy when you run app.py
-- But here's what they'll look like:

-- Products table (auto-created)
-- CREATE TABLE products (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(200) NOT NULL,
--     price NUMERIC(10, 2) NOT NULL,
--     category VARCHAR(100) NOT NULL,
--     created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
-- );

-- Logs table (auto-created)
-- CREATE TABLE logs (
--     id SERIAL PRIMARY KEY,
--     action VARCHAR(50) NOT NULL,
--     product_name VARCHAR(200) NOT NULL,
--     product_price NUMERIC(10, 2),
--     product_category VARCHAR(100),
--     timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
-- );
