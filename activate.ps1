# activate.ps1
# This script automatically navigates to the backend folder and activates the Python Virtual Environment

Write-Host "Navigating to backend directory and activating virtual environment..." -ForegroundColor Cyan

# Check if the .venv folder exists
if (Test-Path "$PSScriptRoot\backend\.venv") {
    # Change directory to backend
    Set-Location -Path "$PSScriptRoot\backend"
    
    # Run the activation script
    . ".\.venv\Scripts\Activate.ps1"
    
    Write-Host "Virtual environment activated successfully!" -ForegroundColor Green
} else {
    Write-Error "Virtual environment not found at $PSScriptRoot\backend\.venv. Have you run 'python -m venv .venv'?"
}
