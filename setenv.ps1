# setenv.ps1 - Set up environment for InquiryCircle project

# Change to project directory
Set-Location -Path "C:\Users\scott\CascadeProjects\InquiryCircle"

Write-Host "Checking if virtual environment is active..."

# Check if we're already in a virtual environment
if (Test-Path env:VIRTUAL_ENV) {
    Write-Host "Virtual environment is already active."
} else {
    Write-Host "Activating virtual environment..."
    if (Test-Path "venv\Scripts\Activate.ps1") {
        try {
            # Enable script execution for this session if needed
            Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
            . "venv\Scripts\Activate.ps1"
            Write-Host "Virtual environment activated successfully."
        } catch {
            Write-Error "Failed to activate virtual environment: $_"
            exit 1
        }
    } else {
        Write-Host "Virtual environment not found. Please create it first with:"
        Write-Host "python -m venv venv"
        exit 1
    }
}

Write-Host ""
Write-Host "Environment is ready for InquiryCircle development."
Write-Host "To start the development server, run: python manage.py runserver"
