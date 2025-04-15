#!/bin/bash

# Script for installing Python virtual environment and required dependencies
set -e

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=========================================${NC}"
echo -e "${GREEN}Installing Python Virtual Environment${NC}"
echo -e "${YELLOW}=========================================${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 is not installed. Please install Python 3.6+ and try again.${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}Detected Python version: ${PYTHON_VERSION}${NC}"

# Check if venv module is available
if ! python3 -c "import venv" &> /dev/null; then
    echo -e "${RED}The venv module is not available. Install it using your package manager (e.g., apt install python3-venv).${NC}"
    exit 1
fi

# Path to virtual environment folder
VENV_DIR="venv"

# Check if venv already exists
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Do you want to delete it and create a new one? (y/n)${NC}"
    read -r answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Deleting existing environment...${NC}"
        rm -rf "$VENV_DIR"
    else
        echo -e "${GREEN}Using existing environment.${NC}"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${GREEN}Creating virtual environment in folder '$VENV_DIR'...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}Virtual environment has been created.${NC}"
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash or similar)
    source "$VENV_DIR/Scripts/activate"
else
    # Linux/Mac
    source "$VENV_DIR/bin/activate"
fi

# Update pip
echo -e "${GREEN}Updating pip...${NC}"
pip install --upgrade pip

# Install required dependencies
echo -e "${GREEN}Installing required dependencies...${NC}"
pip install -r requirements.txt

echo -e "${YELLOW}=========================================${NC}"
echo -e "${GREEN}Installation completed successfully!${NC}"
echo -e "${YELLOW}=========================================${NC}"
echo ""
echo -e "To activate the virtual environment, use:"
echo -e "${YELLOW}source $VENV_DIR/bin/activate${NC} (Linux/Mac)"
echo -e "or"
echo -e "${YELLOW}source $VENV_DIR/Scripts/activate${NC} (Windows)"
echo ""
echo -e "To run scripts after activating the environment, use for example:"
echo -e "${YELLOW}python check_ollama.py${NC}"
echo ""
echo -e "To deactivate the environment, use:"
echo -e "${YELLOW}deactivate${NC}" 