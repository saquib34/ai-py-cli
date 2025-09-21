# AI Terminal Documentation

## Project Structure

This document describes the organization and purpose of each directory in the AI Terminal project.

## Directory Structure

### `/core` - Core Modules
- **`ai/`** - AI processing (`gemini.py`)
- **`db/`** - Database operations (`history.py`)
- **`utils/`** - Shared utilities
  - `kernel.py` - Command execution kernel
  - `monitor.py` - System monitoring tools (CPU, memory, processes, disk, network)

### `/terminal` - Terminal System
- **`cli/`** - Command line interface (`cli.py`)
- **`daemon/`** - Background daemon (`daemon.py`)

### `/scripts` - Utility Scripts
- **`setup_windows.bat`** - Windows setup script

### `/docs` - Documentation
- This directory contains project documentation

## Configuration Files

- **`requirements.txt`** - Python dependencies
- **`main.py`** - Entry point (daemon and CLI modes)
- **`.env`** - Environment variables (API keys, etc.)
- **`.gitignore`** - Git ignore patterns

## Usage

See `README.md` for detailed usage instructions.

## Architecture

The AI Terminal consists of:

1. **CLI** - Command line interface with intelligent autosuggestion
2. **Daemon** - Background service for AI processing and command execution
3. **Database** - SQLite database for command history and metadata
4. **AI Integration** - Google Gemini for natural language command processing
5. **System Monitoring** - Built-in tools for system resource monitoring

## System Monitoring Commands

The terminal includes comprehensive system monitoring capabilities:

- `cpu` - CPU usage, core count, and frequency information
- `mem` - Memory usage statistics (used, total, available)
- `ps` - List of running processes with CPU/memory usage
- `disk` - Disk usage information for all mounted drives
- `network` - Network I/O statistics (bytes sent/received)
- `sysinfo` - System information (OS, Python version, hostname)
- `uptime` - System uptime in days, hours, and minutes

### Adding New Features
1. Core logic goes in `/core`
2. Terminal-specific code in `/terminal`
3. Setup scripts in `/scripts`

### Testing
- Run daemon: `python main.py daemon`
- Run CLI: `python main.py`
- Test autosuggestion: `suggest <command>`