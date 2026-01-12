@echo off
REM PBSC-Ignite Platform - Windows Startup Script

echo ============================================================
echo   PBSC-Ignite - AI-Powered Career Readiness Platform
echo ============================================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Please run setup first: python setup.py
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
echo Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Check MongoDB connection
echo Checking MongoDB connection...
python -c "from pymongo import MongoClient; import os; from dotenv import load_dotenv; load_dotenv(); client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'), serverSelectionTimeoutMS=2000); client.server_info(); print('MongoDB: OK')" 2>nul
if errorlevel 1 (
    echo [WARNING] MongoDB connection failed!
    echo Please ensure MongoDB is running.
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" (
        pause
        exit /b 1
    )
)

echo.
echo ============================================================
echo   Starting PBSC-Ignite Platform...
echo ============================================================
echo.
echo   Access the application at: http://localhost:5000
echo   Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

REM Start the Flask application
python run.py

REM Deactivate virtual environment on exit
deactivate
