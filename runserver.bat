@echo off
REM runserver.bat - Start Django development server for InquiryCircle project

echo Setting up InquiryCircle environment...
call setenv.bat

if errorlevel 1 (
    echo Failed to set up environment
    exit /b 1
)

echo Starting Django development server...
echo.
echo Server will be available at: http://127.0.0.1:8000/
echo Press CTRL+C to stop the server
echo.

python manage.py runserver
