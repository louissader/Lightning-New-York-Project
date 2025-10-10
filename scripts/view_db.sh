#!/bin/bash

# Script to view PostgreSQL database for LNY Product Management System

export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        LNY Product Management - Database Viewer            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Function to display menu
show_menu() {
    echo "What would you like to view?"
    echo ""
    echo "1) All Products"
    echo "2) All Logs (Activity History)"
    echo "3) Products by Category"
    echo "4) Database Statistics"
    echo "5) Table Structure"
    echo "6) Interactive SQL Shell"
    echo "7) Exit"
    echo ""
    read -p "Enter choice [1-7]: " choice
}

# Main loop
while true; do
    show_menu

    case $choice in
        1)
            echo ""
            echo "📦 All Products:"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            psql lny_products -c "SELECT * FROM products ORDER BY created_at DESC;"
            echo ""
            ;;
        2)
            echo ""
            echo "📋 Activity Logs:"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            psql lny_products -c "SELECT * FROM logs ORDER BY timestamp DESC LIMIT 20;"
            echo ""
            ;;
        3)
            echo ""
            echo "📊 Products Grouped by Category:"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            psql lny_products -c "SELECT category, COUNT(*) as count, AVG(price) as avg_price, MIN(price) as min_price, MAX(price) as max_price FROM products GROUP BY category ORDER BY count DESC;"
            echo ""
            ;;
        4)
            echo ""
            echo "📈 Database Statistics:"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            psql lny_products -c "SELECT
                (SELECT COUNT(*) FROM products) as total_products,
                (SELECT COUNT(DISTINCT category) FROM products) as total_categories,
                (SELECT AVG(price)::numeric(10,2) FROM products) as avg_price,
                (SELECT SUM(price)::numeric(10,2) FROM products) as total_value;"
            echo ""
            ;;
        5)
            echo ""
            echo "🏗️  Table Structure:"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            echo "Products Table:"
            psql lny_products -c "\d products"
            echo ""
            echo "Logs Table:"
            psql lny_products -c "\d logs"
            echo ""
            ;;
        6)
            echo ""
            echo "🖥️  Starting Interactive SQL Shell..."
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "Type SQL commands directly. Type 'exit' or '\q' to return to menu."
            echo ""
            psql lny_products
            ;;
        7)
            echo ""
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo ""
            echo "❌ Invalid choice. Please enter 1-7."
            echo ""
            ;;
    esac
done