#!/bin/bash
# AI Terminal Setup Script for Unix/Linux Systems
# Supports Debian, Ubuntu, Arch, Fedora, SUSE, and macOS

set -e  # Exit on any error

echo "🚀 Setting up AI Terminal for Unix/Linux..."
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Detect OS and package manager
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        PACKAGE_MANAGER="brew"
    elif [[ -f /etc/debian_version ]]; then
        OS="debian"
        PACKAGE_MANAGER="apt"
    elif [[ -f /etc/arch-release ]]; then
        OS="arch"
        PACKAGE_MANAGER="pacman"
    elif [[ -f /etc/fedora-release ]]; then
        OS="fedora"
        PACKAGE_MANAGER="dnf"
    elif [[ -f /etc/redhat-release ]]; then
        OS="rhel"
        PACKAGE_MANAGER="yum"
    elif [[ -f /etc/SuSE-release ]] || [[ -f /etc/sles-release ]]; then
        OS="suse"
        PACKAGE_MANAGER="zypper"
    else
        OS="unknown"
        PACKAGE_MANAGER="unknown"
    fi
}

# Install Python if not available
install_python() {
    print_info "Checking Python installation..."

    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
        print_status "Python 3 found"
        python3 --version
        return 0
    fi

    if command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | grep -oP '\d+\.\d+')
        if [[ $(echo "$PYTHON_VERSION >= 3.7" | bc -l) -eq 1 ]]; then
            PYTHON_CMD="python"
            PIP_CMD="pip"
            print_status "Python found (version $PYTHON_VERSION)"
            python --version
            return 0
        fi
    fi

    print_warning "Python 3.7+ not found. Installing..."

    case $OS in
        "debian")
            print_info "Installing Python on Debian/Ubuntu..."
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv
            ;;
        "arch")
            print_info "Installing Python on Arch Linux..."
            sudo pacman -S --noconfirm python python-pip
            ;;
        "fedora")
            print_info "Installing Python on Fedora..."
            sudo dnf install -y python3 python3-pip
            ;;
        "rhel")
            print_info "Installing Python on RHEL/CentOS..."
            sudo yum install -y python3 python3-pip
            ;;
        "suse")
            print_info "Installing Python on SUSE..."
            sudo zypper install -y python3 python3-pip
            ;;
        "macos")
            print_info "Installing Python on macOS..."
            if ! command -v brew &> /dev/null; then
                print_error "Homebrew not found. Install it first: https://brew.sh/"
                exit 1
            fi
            brew install python3
            ;;
        *)
            print_error "Unsupported OS. Please install Python 3.7+ manually."
            print_info "Visit: https://www.python.org/downloads/"
            exit 1
            ;;
    esac

    # Verify installation
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
        print_status "Python installed successfully"
        python3 --version
    else
        print_error "Failed to install Python"
        exit 1
    fi
}

# Check requirements.txt
check_requirements() {
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found in current directory"
        exit 1
    fi
    print_status "requirements.txt found"
}

# Install Python dependencies
install_dependencies() {
    print_info "Installing Python dependencies..."
    if ! $PIP_CMD install --user -r requirements.txt; then
        print_error "Failed to install dependencies"
        exit 1
    fi
    print_status "Dependencies installed"
}

# Check API key configuration
check_api_key() {
    echo
    print_info "Checking API key configuration..."

    if [ -n "$GEMINI_API_KEY" ]; then
        print_status "GEMINI_API_KEY environment variable is set"
    else
        print_warning "GEMINI_API_KEY environment variable not set"
        echo
        print_info "Get your API key from: https://makersuite.google.com/app/apikey"
        echo
        print_info "Set the environment variable:"
        echo "  export GEMINI_API_KEY=your-api-key-here"
        echo
        print_info "Or add to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
        echo "  echo 'export GEMINI_API_KEY=your-api-key-here' >> ~/.bashrc"
        echo "  source ~/.bashrc"
    fi

    # Check .env file
    if [ -f ".env" ]; then
        if grep -q "^GEMINI_API_KEY=" .env; then
            print_status "API key found in .env file"
        else
            print_warning ".env file exists but no GEMINI_API_KEY found"
            echo "Add to .env file: GEMINI_API_KEY=your-api-key-here"
        fi
    else
        print_info "No .env file found. Creating one..."
        echo "# AI Terminal Configuration" > .env
        echo "GEMINI_API_KEY=your-api-key-here" >> .env
        print_info "Created .env file. Please edit it with your actual API key."
    fi
}

# Run validation tests
run_validation() {
    echo
    print_info "Running validation tests..."

    # Test Python imports
    if $PYTHON_CMD -c "
import sys
print(f'Python {sys.version.split()[0]}')
try:
    import google.generativeai
    print('✅ Gemini AI import successful')
except ImportError as e:
    print(f'❌ Gemini AI import failed: {e}')
    sys.exit(1)

try:
    import sqlite3
    print('✅ SQLite import successful')
except ImportError as e:
    print(f'❌ SQLite import failed: {e}')
    sys.exit(1)

print('✅ All imports successful')
"; then
        print_status "Validation passed!"
    else
        print_error "Validation failed"
        exit 1
    fi
}

# Create desktop shortcut (Linux only)
create_shortcut() {
    if [[ "$OS" != "macos" ]] && [[ -n "$DISPLAY" ]]; then
        echo
        print_info "Creating desktop shortcut..."

        DESKTOP_FILE="$HOME/Desktop/ai-terminal.desktop"
        cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=AI Terminal
Comment=Intelligent Command Line Interface
Exec=$PWD/start_ai_terminal.sh
Icon=terminal
Terminal=true
Categories=Utility;TerminalEmulator;
EOF

        chmod +x "$DESKTOP_FILE"
        print_status "Desktop shortcut created: $DESKTOP_FILE"
    fi
}

# Create startup script
create_startup_script() {
    echo
    print_info "Creating startup script..."

    cat > start_ai_terminal.sh << 'EOF'
#!/bin/bash
# AI Terminal Launcher Script

echo "🚀 Starting AI Terminal..."
echo

# Check if daemon is running
if pgrep -f "main.py daemon" > /dev/null; then
    echo "✅ Daemon is already running"
else
    echo "🔄 Starting daemon..."
    nohup python main.py daemon > daemon.log 2>&1 &
    sleep 2
fi

# Start CLI
echo "💻 Starting CLI..."
python main.py
EOF

    chmod +x start_ai_terminal.sh
    print_status "Startup script created: start_ai_terminal.sh"
}

# Main setup function
main() {
    detect_os
    print_info "Detected OS: $OS ($PACKAGE_MANAGER)"
    echo

    install_python
    check_requirements
    install_dependencies
    check_api_key
    run_validation
    create_startup_script

    if [[ "$OS" != "macos" ]]; then
        create_shortcut
    fi

    echo
    print_status "Setup complete!"
    echo
    echo "🎯 Quick Start:"
    echo "  ./start_ai_terminal.sh"
    echo
    echo "💡 Manual Start:"
    echo "  1. Start daemon: python main.py daemon &"
    echo "  2. Start CLI: python main.py"
    echo
    echo "💡 Commands:"
    echo "   • Natural language: 'open google chrome'"
    echo "   • Get suggestions: 'suggest open'"
    echo "   • View history: 'history'"
    echo
    print_info "For more info, see README.md"
    echo
    print_info "Don't forget to set your GEMINI_API_KEY in the .env file!"
}

# Run main function
main "$@"