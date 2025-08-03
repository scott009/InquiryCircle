@echo off
REM Execute the v1.1.0 release process

echo Executing InquiryCircle v1.1.0 release...
echo ======================================

cd /d "C:\Users\scott\CascadeProjects\InquiryCircle"

REM Run the complete release script
release_v1.1.0.bat

echo.
echo Release execution completed.
echo Please check the output above for any errors.
echo If successful, v1.1.0 is now released on GitHub.
echo.
pause
