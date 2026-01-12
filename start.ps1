# Startup script for CSC506 Portfolio System

Write-Host "========================================"
Write-Host "CSC506 Portfolio System Startup"
Write-Host "========================================"
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..."
pip install Flask==3.0.0 Flask-CORS==4.0.0

# Start the application
Write-Host ""
Write-Host "Starting Flask application..."
Write-Host ""
Write-Host "Application will be available at: http://localhost:5000"
Write-Host "Press Ctrl+C to stop the server"
Write-Host ""
python app.py

