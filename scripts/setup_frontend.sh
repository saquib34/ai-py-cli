#!/bin/bash

echo "Setting up AI Terminal Frontend..."
echo

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

if [ ! -d "frontend" ]; then
    echo "Error: Frontend directory not found. Please ensure you're in the project root."
    exit 1
fi

cd frontend

echo "Installing Node.js dependencies..."
if command -v npm &> /dev/null; then
    npm install
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies with npm"
        exit 1
    fi
elif command -v yarn &> /dev/null; then
    yarn install
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies with yarn"
        exit 1
    fi
else
    echo "Error: Neither npm nor yarn is installed. Please install Node.js first."
    exit 1
fi

echo
echo "Frontend setup complete!"
echo
echo "To start the development server, run:"
echo "  cd frontend"
echo "  npm run dev"
echo
echo "Then open http://localhost:3000 in your browser"
echo