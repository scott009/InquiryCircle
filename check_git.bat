@echo off
REM Check if git is installed and available
echo Checking for git installation...
git --version >nul 2>&1
if %errorlevel% == 0 (
    echo Git is installed
    git --version
    
    REM Check if we're in a git repository
    git status >nul 2>&1
    if %errorlevel% == 0 (
        echo Current directory is a git repository
    ) else (
        echo Current directory is NOT a git repository
    )
) else (
    echo Git is not installed or not in PATH
)
