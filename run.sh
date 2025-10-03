#!/bin/bash
# Script to run the LNY Product Management Application

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting LNY Product Management Application${NC}"

# Add PostgreSQL to PATH
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"

# Activate virtual environment
source .venv/bin/activate

# Check if PostgreSQL is running
if ! brew services list | grep postgresql@15 | grep started > /dev/null; then
    echo -e "${BLUE}Starting PostgreSQL service...${NC}"
    brew services start postgresql@15
    sleep 2
fi

# Run the Flask application
echo -e "${GREEN}✅ Starting Flask server...${NC}"
echo -e "${GREEN}🌐 Open your browser to: http://localhost:5000${NC}"
echo -e "${BLUE}Press Ctrl+C to stop the server${NC}"
echo ""

python app.py
