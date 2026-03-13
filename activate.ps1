# activate.ps1
# This script automatically navigates to the RAG folder and activates the Python Virtual Environment

Write-Host "Navigating to RAG directory and activating virtual environment..." -ForegroundColor Cyan

# Check if the .venv folder exists
if (Test-Path "$PSScriptRoot\RAG\.venv") {
    # Change directory to RAG
    Set-Location -Path "$PSScriptRoot\RAG"
    
    # Run the activation script
    . ".\.venv\Scripts\Activate.ps1"
    
    Write-Host "Virtual environment activated successfully!" -ForegroundColor Green
} else {
    Write-Error "Virtual environment not found at $PSScriptRoot\RAG\.venv. Have you run 'python -m venv .venv'?"
}
