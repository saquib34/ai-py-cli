@echo off
echo Setting up AI Terminal Frontend for Windows...
echo.

cd /d "%~dp0.."

if not exist "frontend" (
    echo Frontend directory not found. Please ensure you're in the project root.
    pause
    exit /b 1
)

cd frontend

echo Installing Node.js dependencies...
call npm install

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Frontend setup complete!
echo.
echo To start the development server, run:
echo   cd frontend
echo   npm run dev
echo.
echo Then open http://localhost:3000 in your browser
echo.
pause