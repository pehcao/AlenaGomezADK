@echo off
REM ADK Sales Agent - Windows Setup Script
REM This script sets up the development environment for the ADK Sales Agent API

echo ========================================
echo  ADK Sales Agent - Setup Script
echo ========================================
echo.

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

python --version
echo [SUCCESS] Python found

REM Check if we're in the right directory
if not exist "api\main.py" (
    echo [ERROR] Please run this script from the project root directory
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo [INFO] Setting up virtual environment...
if exist "venv" (
    echo [WARNING] Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)

echo [SUCCESS] Virtual environment created

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo [INFO] Installing dependencies...
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [SUCCESS] Dependencies installed successfully

REM Setup environment file
echo.
echo [INFO] Setting up environment configuration...
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo [WARNING] Created .env from .env.example template
        echo [WARNING] Please edit .env file with your actual Airtable API credentials
    ) else (
        echo [INFO] Creating basic .env file...
        (
            echo # ADK Sales Agent API - Environment Variables
            echo # Copy this file to .env and fill in your actual values
            echo.
            echo # AIRTABLE_API_KEY=your_airtable_api_key_here
            echo AIRTABLE_BASE_ID=appYKRoIWJLctlUdw
            echo AIRTABLE_LEADS_TABLE_ID=tblUZkxzC0MbJ12HG
            echo AIRTABLE_CALLS_TABLE_ID=tblyyuYfdzGc0CAkO
            echo.
            echo # Server Configuration
            echo HOST=0.0.0.0
            echo PORT=8000
            echo DEBUG=false
            echo LOG_LEVEL=INFO
        ) > .env
        echo [WARNING] Created basic .env file - please add your AIRTABLE_API_KEY
    )
) else (
    echo [SUCCESS] Environment file (.env) already exists
)

REM Display final instructions
echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo ✅ Virtual environment created
echo ✅ Dependencies installed
echo ✅ Environment configuration ready
echo.
echo Next Steps:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Edit .env file with your Airtable API key:
echo    notepad .env
echo.
echo 3. Start the development server:
echo    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo 4. Access the API documentation:
echo    http://localhost:8000/docs
echo.
echo 5. Run tests:
echo    python -m pytest test_api.py -v
echo.
echo Happy coding! 🚀
echo.
pause 