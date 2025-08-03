@echo off
REM Run the v1.1.0 release process

echo Running InquiryCircle v1.1.0 release...
echo =====================================

cd /d "C:\Users\scott\CascadeProjects\InquiryCircle"

REM Execute the complete release process
echo 1. Checking git status...
echo ==========================
powershell -ExecutionPolicy Bypass -File "check_git_status.ps1"

echo.
echo 2. Adding and committing changes...
echo ================================
git add .
git commit -m "Release v1.1.0 - CircleMessage1 Feature"

echo.
echo 3. Pushing to GitHub...
echo ======================
git push origin main

echo.
echo 4. Tagging release...
echo ====================
powershell -ExecutionPolicy Bypass -File "tag_release.ps1"

echo.
echo 5. Pushing tags to GitHub...
echo ===========================
git push --tags

echo.
echo Release v1.1.0 completed successfully!
echo Please check GitHub for the new release.
echo.
pause
