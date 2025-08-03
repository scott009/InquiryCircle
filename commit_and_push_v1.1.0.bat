@echo off
REM Commit and push v1.1.0 changes to existing repository

echo Committing and pushing v1.1.0 changes...
cd /d "C:\Users\scott\CascadeProjects\InquiryCircle"

echo Adding all files...
git add .

echo Committing changes...
git commit -m "Release v1.1.0 - CircleMessage1 Feature"

echo Pushing to GitHub...
git push origin main

echo.
echo Changes pushed successfully!
echo.
echo To tag the release, run: tag_release.ps1
echo.
pause
