# AI Terminal - Intelligent Command Line Interface

A cross-platform AI-augmented terminal w## 📊 System Monitoring Commands

The AI Terminal includes built-in system monitoring tools powered by `psutil`:

```bash
ai-os> cpu              # Show CPU usage, cores, and frequency
ai-os> mem              # Display memory usage statistics
ai-os> ps               # List running processes with CPU/memory usage
ai-os> disk             # Show disk usage information
ai-os> network          # Display network I/O statistics
ai-os> sysinfo          # Show system information (OS, Python version, hostname)
ai-os> uptime           # Display system uptime
```

**Example Output:**
```bash
ai-os> cpu
CPU Usage: 15.2%
Cores: 8
Frequency: 3200MHz

ai-os> mem
Memory: 45.2% used
Used: 7.3GB
Total: 16.0GB
Available: 8.7GB

ai-os> ps
1: System (CPU: 0.1%, MEM: 0.2%)
4: python.exe (CPU: 25.3%, MEM: 15.7%)
1234: chrome.exe (CPU: 5.2%, MEM: 8.9%)
...
```nt command suggestions, natural language processing, and database-backed history.

## ✨ Features

- **🤖 AI-Powered Commands**: Natural language to shell command translation using Google Gemini
- **📊 System Monitoring**: Built-in commands for CPU, memory, processes, disk, and network monitoring
- **💻 Web Frontend**: Modern React Next.js terminal interface with typing effects and multiple themes
- **📚 Smart Autosuggestion**: Database-driven command completion with history prioritization
- **🔄 Cross-Platform**: Works on Windows, Linux, and macOS
- **💾 Persistent History**: SQLite database stores command history and execution results
- **🛡️ Safety Checks**: AI validates commands for potential harm
- **⚡ Fast Execution**: Background daemon for instant command processing

## 🏗️ Architecture

```
AI Terminal System
├── CLI (Command Line Interface)
│   ├── Intelligent completion
│   ├── Manual suggestion commands
│   └── History browsing
├── Daemon (Background Service)
│   ├── Socket-based communication
│   ├── AI command processing
│   └── Database storage
└── Database (SQLite)
    ├── Command history
    ├── Execution results
    └── User preferences
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+ (for backend)
- Node.js 18+ (for frontend)
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/saquib34/ai-py-cli.git
   cd ai-py-cli
   ```

2. **Backend Setup**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt

   # Set up environment
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

3. **Frontend Setup** (Optional)
   ```bash
   # Navigate to frontend directory
   cd frontend

   # Install Node.js dependencies
   npm install

   # Return to root directory
   cd ..
   ```

### Usage

#### Backend Only (CLI)
1. **Start the daemon** (in one terminal):
   ```bash
   python main.py daemon
   ```

2. **Start the CLI** (in another terminal):
   ```bash
   python main.py
   ```

#### Full Stack (Web + Backend)
1. **Start the backend daemon**:
   ```bash
   python main.py daemon
   ```

2. **Start the web frontend** (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open browser**: `http://localhost:3000`

#### Use natural language commands:
```bash
ai-os> create a file called test.txt
ai-os> list files
```

## 🌐 Web Frontend Setup

The AI Terminal includes a modern web-based interface built with React Next.js, featuring typing effects, multiple themes, and full customization.

### Prerequisites
- Node.js 18+
- npm or yarn

### Frontend Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/saquib34/ai-py-cli.git
   cd ai-py-cli/frontend
   ```

2. **Run the setup script**
   ```bash

   # For Linux/macOS
   ../scripts/setup_frontend.sh
   ```

3. **Or install manually**
   ```bash
   # Install Node.js dependencies
   npm install
   # or
   yarn install
   ```

4. **Start development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   ```
   http://localhost:3000
   ```

### Frontend Features

- **🎨 Multiple Themes**: Dark, Light, Matrix, and Retro themes
- **⚡ Typing Effects**: Realistic terminal typing animation
- **🎯 Command History**: Navigate with arrow keys
- **📝 Tab Completion**: Auto-complete common commands
- **🔧 Fully Customizable**: Change prompts, fonts, and layouts
- **📱 Responsive Design**: Works on desktop and mobile
- **🎪 Fullscreen Mode**: Immersive terminal experience

### Frontend Commands

```bash
# Basic commands
help              # Show all available commands
clear             # Clear the terminal
history           # View command history
echo <text>       # Display text
date              # Show current date/time
whoami            # Show current user

# System monitoring
cpu               # Display CPU information
mem               # Show memory usage
ps                # List running processes
disk              # Display disk usage
network           # Show network statistics
sysinfo           # Display system information
uptime            # Show system uptime

# Customization
theme <name>      # Change theme (dark, light, matrix, retro)
prompt <text>     # Change command prompt
fontsize <size>   # Change font size (10-24px)
fullscreen        # Toggle fullscreen mode
```

### Connecting Frontend to Backend

To connect the web frontend with the Python backend:

1. **Start the Python daemon** (in one terminal):
   ```bash
   python main.py daemon
   ```

2. **Start the frontend** (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Update API endpoints** in `frontend/src/components/Terminal.tsx`:
   ```typescript
   const response = await fetch('http://localhost:5000/api/command', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ command: args })
   });
   ```

## � System Monitoring Commands

The AI Terminal includes built-in system monitoring tools:

```bash
ai-os> cpu          # Show CPU usage, cores, and frequency
ai-os> mem          # Display memory usage statistics
ai-os> ps           # List running processes with CPU/memory usage
ai-os> disk         # Show disk usage information
ai-os> network      # Display network I/O statistics
ai-os> sysinfo      # Show system information (OS, Python version, hostname)
ai-os> uptime       # Display system uptime
```

## �💡 Autosuggestion System

### Tab Completion (Linux/macOS)
- Press `Tab` to see suggestions
- Prioritizes recent commands from history
- Falls back to available system commands

### Manual Suggestions (Windows/All Platforms)
```bash
ai-os> suggest open
💡 Suggestions:
  1. open google chrome
  2. open notepad
  3. open explorer
```

### History Commands
```bash
ai-os> history          # View recent commands
ai-os> suggest <text>   # Get suggestions manually
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key for AI features | Yes |

### Database

- **Location**: `history.db` (created automatically)
- **Tables**: Command history, execution metadata
- **Backup**: Copy `history.db` to backup your command history

## 📁 Project Structure

```
ai-terminal/
├── core/                    # Core modules
│   ├── ai/                 # AI processing (Gemini)
│   ├── db/                 # Database operations
│   └── utils/              # Utilities and kernel
│       ├── kernel.py       # Command execution kernel
│       └── monitor.py      # System monitoring tools
├── terminal/               # Terminal system
│   ├── cli/               # Command line interface
│   └── daemon/            # Background daemon
├── frontend/               # React Next.js web interface
│   ├── src/
│   │   ├── app/           # Next.js app router
│   │   └── components/    # React components
│   ├── public/            # Static assets
│   └── package.json       # Frontend dependencies
├── scripts/               # Setup scripts
│   ├── setup.sh           # Cross-platform setup (Windows/macOS/Linux)
│   └── setup_unix.sh      # Advanced Unix/Linux setup
├── docs/                  # Documentation
├── main.py                # Entry point
├── setup.sh              # Universal setup launcher
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠️ Development

### Adding New Commands
1. Add handler to `core/utils/kernel.py`
2. Update command discovery in `discover_commands()`
3. Test with daemon running

### AI Prompt Customization
- Edit prompts in `core/ai/gemini.py`
- Test changes with `scripts/test_ai_process.py`

### Database Schema
- History table: command, result, timestamp, success
- Automatic migration on startup

## 🔒 Security

- **API Key Protection**: Never commit `.env` file
- **Command Validation**: AI checks for dangerous operations
- **Input Sanitization**: All inputs validated before execution
- **Database Encryption**: Consider encrypting sensitive history

## 🐛 Troubleshooting

### Common Issues

**"Connection error: [WinError 10054]"**
- Daemon not running: Start with `python main.py daemon`

**"AI import failed"**
- Missing API key: Set `GEMINI_API_KEY` in `.env`
- Install dependencies: `pip install -r requirements.txt`

**"Tab completion not working"**
- On Windows: Use `suggest <command>` instead
- On Linux/macOS: Ensure `readline` is installed

**"Database locked"**
- Close other terminal instances
- Restart daemon to release lock

### Debug Mode
```bash
# Enable verbose logging
python main.py daemon  # Check daemon output
python main.py         # Check CLI output
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.

## ⚠️ Disclaimer

This tool executes system commands with AI assistance. While safety measures are implemented, review AI interpretations for potentially harmful operations. Use at your own risk.