# Command Kernel - Dynamic command discovery and AI-powered suggestions

import os
import shutil
import subprocess
import time
from typing import Dict, List, Optional, Tuple

# Import AI processing
try:
    from core.ai.gemini import ai_process_command, needs_confirmation
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Import system monitoring functions
try:
    from core.utils.monitor import cpu, mem, ps, disk, network, system_info, uptime
    MONITOR_AVAILABLE = True
except ImportError:
    MONITOR_AVAILABLE = False

class CommandKernel:
    """
    Intelligent command kernel that dynamically discovers available commands
    and provides AI-powered suggestions when commands fail.
    """

    def __init__(self):
        self.available_commands = {}
        self.command_cache = {}
        self.cache_timeout = 300  # 5 minutes
        self.last_cache_update = 0
        self._load_basic_commands()

    def _load_basic_commands(self):
        """Load essential built-in commands that are always available"""
        self.available_commands = {
            'help': {
                'type': 'builtin',
                'description': 'Show help information',
                'handler': self._help_handler
            },
            'commands': {
                'type': 'builtin',
                'description': 'List all available commands',
                'handler': self._commands_handler
            },
            'refresh': {
                'type': 'builtin',
                'description': 'Refresh command cache',
                'handler': lambda: self._refresh_handler()
            },
            'exit': {
                'type': 'builtin',
                'description': 'Exit the terminal',
                'handler': lambda: 'exit'
            },
            'clear': {
                'type': 'builtin',
                'description': 'Clear the screen',
                'handler': lambda: '\033[2J\033[H'
            }
        }

        # Add system monitoring commands if available
        if MONITOR_AVAILABLE:
            monitoring_commands = {
                'cpu': {
                    'type': 'builtin',
                    'description': 'Show CPU usage and information',
                    'handler': lambda: cpu()
                },
                'mem': {
                    'type': 'builtin',
                    'description': 'Show memory usage statistics',
                    'handler': lambda: mem()
                },
                'ps': {
                    'type': 'builtin',
                    'description': 'List running processes',
                    'handler': lambda: ps()
                },
                'disk': {
                    'type': 'builtin',
                    'description': 'Show disk usage information',
                    'handler': lambda: disk()
                },
                'network': {
                    'type': 'builtin',
                    'description': 'Show network I/O statistics',
                    'handler': lambda: network()
                },
                'sysinfo': {
                    'type': 'builtin',
                    'description': 'Show system information',
                    'handler': lambda: system_info()
                },
                'uptime': {
                    'type': 'builtin',
                    'description': 'Show system uptime',
                    'handler': lambda: uptime()
                }
            }
            self.available_commands.update(monitoring_commands)

    def discover_commands(self) -> Dict[str, dict]:
        """
        Dynamically discover available commands from system PATH and common locations
        """
        current_time = time.time()

        # Use cache if it's still valid
        if current_time - self.last_cache_update < self.cache_timeout:
            return self.available_commands

        print("🔍 Discovering available commands...")

        # Common command categories to check
        command_categories = {
            'development': ['python', 'python3', 'pip', 'pip3', 'node', 'npm', 'yarn', 'git', 'docker', 'docker-compose'],
            'system': ['ps', 'top', 'htop', 'kill', 'killall', 'ping', 'netstat', 'ss', 'curl', 'wget'],
            'file_ops': ['ls', 'cd', 'pwd', 'mkdir', 'rm', 'cp', 'mv', 'cat', 'head', 'tail', 'grep', 'find'],
            'text_editors': ['vim', 'nano', 'emacs', 'code', 'notepad', 'gedit'],
            'browsers': ['firefox', 'chrome', 'chromium', 'safari', 'opera'],
            'package_managers': ['apt', 'yum', 'dnf', 'pacman', 'brew', 'snap', 'flatpak'],
            'network': ['ssh', 'scp', 'ftp', 'sftp', 'telnet'],
            'compression': ['tar', 'gzip', 'zip', 'unzip', 'rar', '7z']
        }

        discovered = dict(self.available_commands)  # Start with built-ins

        # Add shell builtins that aren't external executables
        shell_builtins = {
            'cd': {'type': 'builtin', 'category': 'file_ops', 'description': 'Change directory'},
            'exit': {'type': 'builtin', 'category': 'system', 'description': 'Exit the terminal'},
            'cls': {'type': 'builtin', 'category': 'system', 'description': 'Clear screen'},
            'clear': {'type': 'builtin', 'category': 'system', 'description': 'Clear screen'},
            'pwd': {'type': 'builtin', 'category': 'file_ops', 'description': 'Print working directory'},
            'dir': {'type': 'builtin', 'category': 'file_ops', 'description': 'List directory contents'},
            'ls': {'type': 'builtin', 'category': 'file_ops', 'description': 'List directory contents'},
            'echo': {'type': 'builtin', 'category': 'system', 'description': 'Display text'},
            'type': {'type': 'builtin', 'category': 'file_ops', 'description': 'Display file contents'},
            'cat': {'type': 'builtin', 'category': 'file_ops', 'description': 'Display file contents'},
            'copy': {'type': 'builtin', 'category': 'file_ops', 'description': 'Copy files'},
            'cp': {'type': 'builtin', 'category': 'file_ops', 'description': 'Copy files'},
            'move': {'type': 'builtin', 'category': 'file_ops', 'description': 'Move files'},
            'mv': {'type': 'builtin', 'category': 'file_ops', 'description': 'Move files'},
            'del': {'type': 'builtin', 'category': 'file_ops', 'description': 'Delete files'},
            'rm': {'type': 'builtin', 'category': 'file_ops', 'description': 'Delete files'},
            'md': {'type': 'builtin', 'category': 'file_ops', 'description': 'Make directory'},
            'mkdir': {'type': 'builtin', 'category': 'file_ops', 'description': 'Make directory'},
            'rd': {'type': 'builtin', 'category': 'file_ops', 'description': 'Remove directory'},
            'rmdir': {'type': 'builtin', 'category': 'file_ops', 'description': 'Remove directory'},
            'ren': {'type': 'builtin', 'category': 'file_ops', 'description': 'Rename files'},
            'help': {'type': 'builtin', 'category': 'system', 'description': 'Show help'},
            'history': {'type': 'builtin', 'category': 'system', 'description': 'Show command history'},
            'commands': {'type': 'builtin', 'category': 'system', 'description': 'List available commands'},
        }

        # Add Windows-specific shell builtins
        if os.name == 'nt':
            windows_builtins = {
                'start': {'type': 'builtin', 'category': 'system', 'description': 'Start a program or open file'},
            }
            shell_builtins.update(windows_builtins)

        # Add shell builtins to discovered commands
        for cmd, info in shell_builtins.items():
            discovered[cmd] = {
                **info,
                'handler': getattr(self, f'_{cmd}_handler', self._create_shell_builtin_handler(cmd))
            }

        # Add Windows-specific commands and builtins
        windows_builtins = {
            'start': {'type': 'builtin', 'category': 'system', 'description': 'Start a program or open file'},
            'echo.': {'type': 'builtin', 'category': 'system', 'description': 'Create empty file (Windows)'},
            'cls': {'type': 'builtin', 'category': 'system', 'description': 'Clear screen'},
            'copy': {'type': 'builtin', 'category': 'file_ops', 'description': 'Copy files'},
            'move': {'type': 'builtin', 'category': 'file_ops', 'description': 'Move files'},
            'ren': {'type': 'builtin', 'category': 'file_ops', 'description': 'Rename files'},
            'del': {'type': 'builtin', 'category': 'file_ops', 'description': 'Delete files'},
            'type': {'type': 'builtin', 'category': 'file_ops', 'description': 'Display file contents'},
            'more': {'type': 'builtin', 'category': 'file_ops', 'description': 'Display file contents page by page'},
            'find': {'type': 'builtin', 'category': 'file_ops', 'description': 'Search for text in files'},
            'sort': {'type': 'builtin', 'category': 'file_ops', 'description': 'Sort file contents'},
            'fc': {'type': 'builtin', 'category': 'file_ops', 'description': 'Compare files'},
            'tree': {'type': 'builtin', 'category': 'file_ops', 'description': 'Display directory structure'},
            'attrib': {'type': 'builtin', 'category': 'file_ops', 'description': 'Change file attributes'},
            'chdir': {'type': 'builtin', 'category': 'file_ops', 'description': 'Change directory'},
            'mkdir': {'type': 'builtin', 'category': 'file_ops', 'description': 'Make directory'},
            'rmdir': {'type': 'builtin', 'category': 'file_ops', 'description': 'Remove directory'},
            'vol': {'type': 'builtin', 'category': 'system', 'description': 'Display volume information'},
            'ver': {'type': 'builtin', 'category': 'system', 'description': 'Display Windows version'},
            'time': {'type': 'builtin', 'category': 'system', 'description': 'Display or set system time'},
            'date': {'type': 'builtin', 'category': 'system', 'description': 'Display or set system date'},
            'set': {'type': 'builtin', 'category': 'system', 'description': 'Display or set environment variables'},
            'path': {'type': 'builtin', 'category': 'system', 'description': 'Display or set PATH'},
            'prompt': {'type': 'builtin', 'category': 'system', 'description': 'Change command prompt'},
            'title': {'type': 'builtin', 'category': 'system', 'description': 'Set window title'},
            'color': {'type': 'builtin', 'category': 'system', 'description': 'Set console colors'},
        }

        # Add Windows builtins to discovered commands
        for cmd, info in windows_builtins.items():
            discovered[cmd] = {
                **info,
                'handler': self._create_shell_builtin_handler(cmd)
            }

        for category, commands in command_categories.items():
            for cmd in commands:
                if self._is_command_available(cmd):
                    discovered[cmd] = {
                        'type': 'external',
                        'category': category,
                        'description': f'{cmd} command ({category})',
                        'handler': self._create_external_handler(cmd),
                        'path': shutil.which(cmd)
                    }

        # Add Windows-specific commands if on Windows
        if os.name == 'nt':
            windows_cmds = ['cmd', 'powershell', 'explorer', 'notepad', 'calc', 'taskmgr', 'chrome', 'firefox', 'msedge', 'start']
            for cmd in windows_cmds:
                if self._is_command_available(cmd):
                    discovered[cmd] = {
                        'type': 'external',
                        'category': 'windows',
                        'description': f'Windows {cmd}',
                        'handler': self._create_external_handler(cmd),
                        'path': shutil.which(cmd)
                    }

        self.available_commands = discovered
        self.last_cache_update = current_time

        print(f"✅ Discovered {len(discovered)} commands")
        return discovered

    def _is_command_available(self, command: str) -> bool:
        """Check if a command is available in the system"""
        return shutil.which(command) is not None

    def _create_external_handler(self, command: str):
        """Create a handler function for external commands"""
        def handler(args=''):
            try:
                cmd_line = f'{command} {args}'.strip()
                result = subprocess.run(
                    cmd_line,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=os.getcwd()
                )
                return result.stdout if result.stdout else result.stderr
            except subprocess.TimeoutExpired:
                return f'{command}: command timed out after 30 seconds'
            except FileNotFoundError:
                return f'{command}: command not found'
            except Exception as e:
                return f'{command}: error: {e}'
        return handler

    def _create_shell_builtin_handler(self, command: str):
        """Create a handler function for shell builtin commands"""
        def handler(args=''):
            try:
                # Use cmd.exe on Windows for shell builtins
                if os.name == 'nt':
                    cmd_line = f'cmd /c {command} {args}'.strip()
                else:
                    # On Unix-like systems, use the shell directly
                    cmd_line = f'{command} {args}'.strip()

                result = subprocess.run(
                    cmd_line,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=os.getcwd()
                )
                return result.stdout if result.stdout else result.stderr
            except subprocess.TimeoutExpired:
                return f'{command}: command timed out after 30 seconds'
            except FileNotFoundError:
                return f'{command}: command not found'
            except Exception as e:
                return f'{command}: error: {e}'
        return handler

    def _cd_handler(self, args=''):
        """Handle cd command"""
        if not args.strip():
            # cd with no args goes to home directory
            if os.name == 'nt':
                os.chdir(os.path.expanduser('~'))
            else:
                os.chdir(os.path.expanduser('~'))
            return f"Changed directory to {os.getcwd()}"
        else:
            try:
                os.chdir(args.strip())
                return f"Changed directory to {os.getcwd()}"
            except FileNotFoundError:
                return f"cd: {args.strip()}: No such file or directory"
            except OSError as e:
                return f"cd: {e}"

    def _pwd_handler(self, args=''):
        """Handle pwd command"""
        return os.getcwd()

    def _exit_handler(self, args=''):
        """Handle exit command"""
        return "exit"

    def _cls_handler(self, args=''):
        """Handle cls command (Windows)"""
        return "\033[2J\033[H"  # ANSI escape sequence to clear screen

    def _clear_handler(self, args=''):
        """Handle clear command (Unix)"""
        return "\033[2J\033[H"  # ANSI escape sequence to clear screen

    def _echo_handler(self, args=''):
        """Handle echo command"""
        return args

    def _history_handler(self, args=''):
        """Handle history command"""
        if hasattr(self, 'command_history') and self.command_history:
            output = "Command History:\n" + "="*30 + "\n"
            for i, cmd in enumerate(self.command_history[-20:], 1):  # Show last 20 commands
                output += f"{i:2d}. {cmd}\n"
            return output
        else:
            return "No command history available"

    def execute_command(self, command_line: str) -> Tuple[str, bool]:
        """
        Execute a command with intelligent fallback and AI suggestions

        Returns: (output, success)
        """
        parts = command_line.strip().split()
        if not parts:
            return "", True

        command = parts[0].lower()
        args = ' '.join(parts[1:]) if len(parts) > 1 else ''

        # Ensure commands are discovered
        if not self.available_commands or time.time() - self.last_cache_update > self.cache_timeout:
            self.discover_commands()

        # First, try AI to understand natural language commands
        if AI_AVAILABLE and len(command_line.strip()) > 2:  # Only for longer inputs that might be natural language
            print(f"🤖 AI processing: '{command_line.strip()}'")
            ai_command, is_risky = ai_process_command(command_line.strip())
            print(f"🤖 AI result: '{ai_command}' (risky: {is_risky})")
            if ai_command != command_line.strip():  # AI suggested a different command
                print(f"🤖 AI interpreted: '{command_line}' → '{ai_command}'")
                if is_risky:
                    return f"⚠️  Risky command detected: {ai_command}\n💡 This command could be dangerous. Use with caution or try a safer alternative.", False

                # Execute the AI-suggested command directly (don't check available_commands)
                try:
                    # For AI-translated commands, execute them as shell commands
                    result = subprocess.run(
                        ai_command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30,
                        cwd=os.getcwd()
                    )
                    output = result.stdout if result.stdout else result.stderr
                    return f"🤖 AI executed: {ai_command}\n{output}", result.returncode == 0
                except subprocess.TimeoutExpired:
                    return f"🤖 AI command timed out: {ai_command}", False
                except Exception as e:
                    return f"🤖 AI command failed: {ai_command}\n❌ Error: {e}", False
            else:
                print(f"🤖 AI returned same command, continuing with normal processing")
        else:
            print(f"🤖 AI not available or command too short: AI_AVAILABLE={AI_AVAILABLE}, len={len(command_line.strip())}")

        # Check if original command is available
        if command in self.available_commands:
            try:
                handler = self.available_commands[command]['handler']
                if args:
                    result = handler(args)
                else:
                    result = handler()
                return result, True
            except Exception as e:
                error_msg = f"Error executing {command}: {e}"
                suggestion = self._get_ai_suggestion(command_line, str(e))
                return f"{error_msg}\n💡 Suggestion: {suggestion}", False

        # Command not found - try AI suggestion
        suggestion = self._get_ai_suggestion(command_line, "command not found")
        return f"'{command}' is not available.\n💡 Did you mean: {suggestion}", False

    def _get_ai_suggestion(self, original_command: str, error: str) -> str:
        """
        Get AI-powered suggestion for failed commands
        This is a simplified version - in production, this would call Gemini API
        """
        # Simple pattern matching for common mistakes
        suggestions = {
            'ls': ['dir', 'list', 'show files'],
            'cd': ['change directory', 'go to'],
            'mkdir': ['create directory', 'make folder'],
            'rm': ['delete', 'remove'],
            'cp': ['copy', 'duplicate'],
            'mv': ['move', 'rename'],
            'ps': ['processes', 'tasks'],
            'kill': ['stop', 'terminate'],
            'ping': ['test connection', 'check network'],
            'git': ['version control', 'repository'],
            'python': ['run script', 'execute python'],
            'pip': ['install package', 'python package manager']
        }

        original_lower = original_command.lower()

        # Check for exact matches in suggestions
        for cmd, aliases in suggestions.items():
            if any(alias in original_lower for alias in aliases):
                if self._is_command_available(cmd):
                    return f"'{cmd}' (available on your system)"

        # Check for typos in available commands
        available_cmds = list(self.available_commands.keys())
        for cmd in available_cmds:
            # Simple Levenshtein distance for typo detection
            if self._simple_distance(original_command, cmd) <= 2:
                return f"'{cmd}' (did you mean this?)"

        # Generic suggestions based on error type
        if "not found" in error.lower():
            return "Check if the program is installed or try 'help' for available commands"
        elif "permission" in error.lower():
            return "Try running with administrator/sudo privileges"
        elif "timeout" in error.lower():
            return "Command took too long - it might be hanging"
        else:
            return "Try 'help' or 'commands' to see available options"

    def _simple_distance(self, s1: str, s2: str) -> int:
        """Simple Levenshtein distance for typo detection"""
        if len(s1) < len(s2):
            return self._simple_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def _help_handler(self, args=''):
        """Handle help command"""
        if args.strip():
            cmd = args.strip().lower()
            if cmd in self.available_commands:
                info = self.available_commands[cmd]
                return f"Help for '{cmd}':\n  Type: {info['type']}\n  Description: {info['description']}\n  Category: {info.get('category', 'N/A')}"
            else:
                return f"No help available for '{cmd}'"
        else:
            return """AI Terminal Help
================

Available command types:
• Built-in commands (always available)
• External commands (discovered from your system)

Special features:
• AI-powered command suggestions when commands fail
• Dynamic command discovery from system PATH
• Intelligent error handling and recovery

Type 'commands' to see all available commands
Type 'help <command>' for specific help"""

    def _commands_handler(self, args=''):
        """Handle commands command - list all available commands"""
        if not self.available_commands or time.time() - self.last_cache_update > self.cache_timeout:
            self.discover_commands()

        output = "Available Commands:\n" + "="*50 + "\n"

        # Group commands by type
        builtin = []
        external = []

        for cmd, info in self.available_commands.items():
            if info['type'] == 'builtin':
                builtin.append(f"  {cmd:<12} - {info['description']}")
            else:
                category = info.get('category', 'System')
                external.append(f"  {cmd:<12} - {info['description']} ({category})")

        if builtin:
            output += "\nBuilt-in Commands:\n"
            output += "\n".join(builtin)

        if external:
            output += "\n\nExternal Commands:\n"
            output += "\n".join(external)

        output += f"\n\nTotal: {len(self.available_commands)} commands available"
        output += "\n\n💡 Type 'help <command>' for detailed information about a specific command"
        output += "\n💡 AI-powered suggestions available when commands fail"

        return output

    def get_command_info(self, command: str) -> Optional[dict]:
        """Get information about a specific command"""
        return self.available_commands.get(command.lower())

    def refresh_cache(self):
        """Force refresh of command cache"""
        self.last_cache_update = 0
        self.discover_commands()

# Global kernel instance
command_kernel = CommandKernel()