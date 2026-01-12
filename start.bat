@echo off
REM Startup script for CSC506 Portfolio System

echo ========================================
echo CSC506 Portfolio System Startup
echo ========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install Flask==3.0.0 Flask-CORS==4.0.0

REM Start the application
echo.
echo Starting Flask application...
echo.
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause

