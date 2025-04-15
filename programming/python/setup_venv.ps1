# PowerShell script for installing Python virtual environment and required dependencies

# Function for displaying colored messages
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    else {
        $input | Write-Output
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Green "========================================="
Write-ColorOutput Green "Installing Python Virtual Environment"
Write-ColorOutput Green "========================================="

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-ColorOutput Green "Detected $pythonVersion"
}
catch {
    Write-ColorOutput Red "Python is not installed or not available in PATH. Please install Python 3.6+ and try again."
    exit 1
}

# Path to virtual environment folder
$VENV_DIR = "venv"

# Check if venv already exists
if (Test-Path $VENV_DIR) {
    Write-ColorOutput Yellow "Virtual environment already exists. Do you want to delete it and create a new one? (Y/N)"
    $answer = Read-Host
    if ($answer -eq "Y" -or $answer -eq "y") {
        Write-ColorOutput Yellow "Deleting existing environment..."
        Remove-Item -Recurse -Force $VENV_DIR
    }
    else {
        Write-ColorOutput Green "Using existing environment."
    }
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path $VENV_DIR)) {
    Write-ColorOutput Green "Creating virtual environment in folder '$VENV_DIR'..."
    python -m venv $VENV_DIR
    Write-ColorOutput Green "Virtual environment has been created."
}

# Activate virtual environment
Write-ColorOutput Green "Activating virtual environment..."
& "$VENV_DIR\Scripts\Activate.ps1"

# Update pip
Write-ColorOutput Green "Updating pip..."
python -m pip install --upgrade pip

# Install required dependencies
Write-ColorOutput Green "Installing required dependencies..."
pip install -r requirements.txt

Write-ColorOutput Green "========================================="
Write-ColorOutput Green "Installation completed successfully!"
Write-ColorOutput Green "========================================="
Write-Output ""
Write-Output "To activate the virtual environment in the future, use:"
Write-ColorOutput Yellow ".\$VENV_DIR\Scripts\Activate.ps1"
Write-Output ""
Write-Output "To run scripts after activating the environment, use for example:"
Write-ColorOutput Yellow "python check_ollama.py"
Write-Output ""
Write-Output "To deactivate the environment, use:"
Write-ColorOutput Yellow "deactivate" 