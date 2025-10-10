#!/bin/bash

echo "🚀 Starting FastAPI Server (alongside Flask)"
echo ""
echo "📝 What is FastAPI?"
echo "   - Modern Python framework for building APIs"
echo "   - Automatically generates interactive documentation"
echo "   - Faster than Flask for API-only applications"
echo ""
echo "🔄 How it works with your Flask app:"
echo "   - Flask (port 5000): Web interface + API"
echo "   - FastAPI (port 8000): API only + Auto docs"
echo "   - Both share the same PostgreSQL database"
echo ""
echo "✅ Starting FastAPI server..."
echo "🌐 Open your browser to:"
echo "   - API: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs (interactive!)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Activate virtual environment and run
source .venv/bin/activate
python fastapi_app.py
