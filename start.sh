#!/bin/bash
# PBSC-Ignite Platform - Linux/Mac Startup Script

echo "============================================================"
echo "  PBSC-Ignite - AI-Powered Career Readiness Platform"
echo "============================================================"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "[ERROR] .env file not found!"
    echo "Please run setup first: python setup.py"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
echo "Checking dependencies..."
if ! pip show flask > /dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Check MongoDB connection
echo "Checking MongoDB connection..."
python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'), serverSelectionTimeoutMS=2000); client.server_info(); print('MongoDB: OK')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[WARNING] MongoDB connection failed!"
    echo "Please ensure MongoDB is running."
    echo ""
    read -p "Continue anyway? (y/n): " continue
    if [ "$continue" != "y" ] && [ "$continue" != "Y" ]; then
        exit 1
    fi
fi

echo ""
echo "============================================================"
echo "  Starting PBSC-Ignite Platform..."
echo "============================================================"
echo ""
echo "  Access the application at: http://localhost:5000"
echo "  Press Ctrl+C to stop the server"
echo ""
echo "============================================================"
echo ""

# Start the Flask application
python run.py

# Deactivate virtual environment on exit
deactivate
