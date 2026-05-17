@echo off
echo ========================================
echo Smart Canteen System - Setup Script
echo ========================================
echo.

echo [1/5] Checking prerequisites...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✓ Python found
echo ✓ Node.js found
echo.

echo [2/5] Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Creating .env file from example...
if not exist .env (
    copy .env.example .env
    echo ✓ Created .env file
    echo IMPORTANT: Please update DATABASE_URL and SECRET_KEY in backend\.env
) else (
    echo .env already exists, skipping...
)

cd ..
echo ✓ Backend setup complete
echo.

echo [3/5] Setting up Frontend...
cd frontend

echo Installing Node dependencies...
call npm install

echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo ✓ Created .env file
) else (
    echo .env already exists, skipping...
)

cd ..
echo ✓ Frontend setup complete
echo.

echo [4/5] Database Setup Instructions...
echo.
echo Please ensure PostgreSQL is installed and running.
echo.
echo To create the database, run:
echo   psql -U postgres
echo   CREATE DATABASE smart_canteen;
echo   \q
echo.
echo Then update DATABASE_URL in backend\.env:
echo   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/smart_canteen
echo.

echo [5/5] Setup Complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Update configuration files:
echo    - backend\.env (DATABASE_URL, SECRET_KEY)
echo    - frontend\.env (REACT_APP_API_URL)
echo.
echo 2. Start the backend:
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn app.main:app --reload
echo.
echo 3. Start the frontend (in a new terminal):
echo    cd frontend
echo    npm start
echo.
echo 4. Access the application:
echo    - Frontend: http://localhost:3000
echo    - Backend API: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo.
echo 5. Default login credentials:
echo    - Email: admin@smartcanteen.com
echo    - Password: admin123
echo.
echo ========================================

pause
