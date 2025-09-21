#!/bin/bash
# Universal AI Terminal Setup Script
# Automatically detects platform and runs appropriate setup

echo "🚀 AI Terminal Universal Setup"
echo

# Detect platform and run appropriate setup
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ "$OS" == "Windows_NT" ]]; then
    echo "🎯 Windows detected"
    echo "Running Windows setup..."
    echo

    # Run the cross-platform bash script
    if [ -f "scripts/setup.sh" ]; then
        bash scripts/setup.sh
    else
        echo "❌ setup.sh not found in scripts directory"
        echo "Please run setup manually:"
        echo "1. Install Python 3.7+ from https://python.org"
        echo "2. pip install -r requirements.txt"
        echo "3. Set GEMINI_API_KEY environment variable"
        exit 1
    fi
else
    echo "🐧 Unix/Linux detected"
    echo "Running Unix setup..."
    echo

    # Run the Unix setup script
    if [ -f "scripts/setup_unix.sh" ]; then
        bash scripts/setup_unix.sh
    else
        echo "❌ setup_unix.sh not found in scripts directory"
        echo "Please install dependencies manually:"
        echo "1. Install Python 3.7+:"
        echo "   Debian/Ubuntu: sudo apt install python3 python3-pip"
        echo "   Arch: sudo pacman -S python python-pip"
        echo "   Fedora: sudo dnf install python3 python3-pip"
        echo "   macOS: brew install python3"
        echo "2. pip3 install -r requirements.txt"
        echo "3. Set GEMINI_API_KEY environment variable"
        exit 1
    fi
fi