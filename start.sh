#!/bin/bash
# Concert Booking System Startup Script

echo "🎵 Starting Concert Booking System..."
echo ""

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Try to initialize database
echo "🔧 Initializing database..."
python init_db.py
echo ""

# Start Flask application
echo "🚀 Starting Flask server on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
python app.py
