#!/bin/bash
# AI Terminal Setup Script (Cross-platform)
# Works on Windows (with bash), Linux, and macOS

echo "🚀 Setting up AI Terminal..."
echo

# Detect platform
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    IS_WINDOWS=true
    PYTHON_CMD="python"
    PIP_CMD="pip"
    PAUSE_CMD="read -p 'Press Enter to continue...'"
else
    IS_WINDOWS=false
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
    PAUSE_CMD="read -p 'Press Enter to continue...'"
fi

# Check if Python is available
echo "🐍 Checking Python installation..."
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.7+"
    echo "   Windows: https://www.python.org/downloads/"
    echo "   Linux: sudo apt install python3 python3-pip"
    echo "   macOS: brew install python3"
    $PAUSE_CMD
    exit 1
fi

# Show Python version
$PYTHON_CMD --version
echo

# Check requirements.txt
if [ ! -f "../requirements.txt" ]; then
    echo "❌ requirements.txt not found in parent directory"
    $PAUSE_CMD
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
if ! $PIP_CMD install -r ../requirements.txt; then
    echo "❌ Failed to install dependencies"
    $PAUSE_CMD
    exit 1
fi

# Check for API key
echo
echo "🔑 Checking API key configuration..."
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY environment variable not set"
    echo "Get your API key from: https://makersuite.google.com/app/apikey"
    echo
    echo "Set the environment variable:"
    if [ "$IS_WINDOWS" = true ]; then
        echo "  Windows: set GEMINI_API_KEY=your-api-key-here"
        echo "  Or permanently: System Properties → Environment Variables"
    else
        echo "  Linux/macOS: export GEMINI_API_KEY=your-api-key-here"
        echo "  Or add to ~/.bashrc or ~/.zshrc: export GEMINI_API_KEY=your-api-key-here"
    fi
    echo
fi

# Check if .env file exists and has the key
if [ -f "../.env" ]; then
    if grep -q "GEMINI_API_KEY=" "../.env"; then
        echo "✅ API key found in .env file"
    else
        echo "⚠️  .env file exists but no GEMINI_API_KEY found"
        echo "Add to .env file: GEMINI_API_KEY=your-api-key-here"
    fi
else
    echo "ℹ️  No .env file found. Create one with your API key:"
    echo "   echo 'GEMINI_API_KEY=your-api-key-here' > .env"
fi

# Run basic validation
echo
echo "🧪 Running basic validation..."
cd ..
if $PYTHON_CMD -c "import sys; print(f'Python {sys.version}'); import google.generativeai; print('✅ Gemini AI import successful')"; then
    echo "✅ Basic validation passed!"
else
    echo "❌ Validation failed. Check your Python installation and dependencies."
    $PAUSE_CMD
    exit 1
fi

echo
echo "✅ Setup complete!"
echo
echo "🎯 To run AI Terminal:"
echo "1. Start daemon: python main.py daemon"
echo "2. Start CLI: python main.py"
echo
echo "💡 Commands:"
echo "   • Type natural language: 'open google chrome'"
echo "   • Get suggestions: 'suggest open'"
echo "   • View history: 'history'"
echo
echo "📚 For more info, see README.md"
echo

$PAUSE_CMD