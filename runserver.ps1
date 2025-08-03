# runserver.ps1 - Start Django development server for InquiryCircle project

Write-Host "Setting up InquiryCircle environment..."

# Change to the backend directory where manage.py is located
Set-Location -Path "C:\Users\scott\CascadeProjects\InquiryCircle\backend"

# Source the environment setup script
. "C:\Users\scott\CascadeProjects\InquiryCircle\setenv.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to set up environment"
    exit 1
}

Write-Host "Starting Django development server..."
Write-Host ""
Write-Host "Server will be available at: http://127.0.0.1:8000/"
Write-Host "Press CTRL+C to stop the server"
Write-Host ""

python manage.py runserver
