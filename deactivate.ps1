# deactivate.ps1
# This script deactivates the Python Virtual Environment and returns to the root folder

Write-Host "Deactivating virtual environment..." -ForegroundColor Cyan

# Check if the deactivate function is available (meaning a venv is currently active)
if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    # Call the built-in deactivate function
    deactivate
    Write-Host "Virtual environment deactivated successfully!" -ForegroundColor Green
} else {
    Write-Host "No virtual environment is currently active." -ForegroundColor Yellow
}

# Return to the root workspace directory
Set-Location -Path "$PSScriptRoot"
Write-Host "Returned to workspace root: $pwd" -ForegroundColor Cyan
