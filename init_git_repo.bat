@echo off
REM Initialize git repository for InquiryCircle project

echo Initializing git repository...
cd /d "C:\Users\scott\CascadeProjects\InquiryCircle"

git init
echo.
echo Adding all files to repository...
git add .
echo.
echo Making initial commit...
git commit -m "Initial commit: InquiryCircle v1.1.0 with CircleMessage1 feature"
echo.
echo Setting up remote repository...
git remote add origin https://github.com/scott009/InquiryCircle.git
echo.
echo Repository initialized successfully!
echo.
echo To push to GitHub, run: git push -u origin main
echo.
pause
