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
- **� System Monitoring**: Built-in commands for CPU, memory, processes, disk, and network monitoring
- **�📚 Smart Autosuggestion**: Database-driven command completion with history prioritization
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
- Python 3.7+
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-terminal
   ```

2. **Run the setup script for your platform**

   **Windows:**
   ```bash
   setup.sh
   # or
   bash scripts/setup.sh
   ```

   **Linux/macOS (Universal):**
   ```bash
   bash scripts/setup_unix.sh
   ```

   **Manual Setup:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

4. **Run setup (Windows)**
   ```bash
   scripts\setup_windows.bat
   ```

### Usage

1. **Start the daemon** (in one terminal):
   ```bash
   python main.py daemon
   ```

2. **Start the CLI** (in another terminal):
   ```bash
   python main.py
   ```

3. **Use natural language commands**:
   ```bash
   ai-os> create a file called test.txt
   ai-os> list files
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
├── scripts/               # Setup scripts
│   ├── setup.sh           # Cross-platform setup (Windows/macOS/Linux)
│   └── setup_unix.sh      # Advanced Unix/Linux setup
├── docs/                  # Documentation
├── main.py                # Entry point
├── setup.sh              # Universal setup launcher
├── requirements.txt       # Dependencies
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