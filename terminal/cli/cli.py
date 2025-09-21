# Try to import readline (Unix-only, optional on Windows)
import os

try:
    import readline
    READLINE_AVAILABLE = True
    print("✅ Readline available - tab completion enabled")
except ImportError:
    READLINE_AVAILABLE = False
    print("⚠️  Readline not available - using fallback completion")
    print("   Type 'suggest <partial>' for manual suggestions")

import socket
import glob
import sys

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))

# Cross-platform socket configuration
if os.name == "nt":  # Windows
    HOST = "127.0.0.1"
    PORT = 65432
    SOCKET_TYPE = "tcp"
    SOCKET_PATH = None
else:  # Unix-like systems (Linux, macOS)
    SOCKET_PATH = "/tmp/aios.sock"
    SOCKET_TYPE = "unix"
    HOST = None
    PORT = None

# History and completion helpers
HIST_FILE = os.path.expanduser("~/.aios_history")

def get_file_history():
    """Get history from file (fallback)"""
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE) as f:
            return [line.strip() for line in f]
    return []

def get_db_history(limit=100):
    """Get command history from database"""
    try:
        from core.db.history import init_db, get_history
        conn = init_db("history.db")
        history_records = get_history(conn, limit=limit)
        conn.close()
        # Extract just the commands
        return [record['command'] for record in history_records if 'command' in record]
    except Exception as e:
        print(f"Database history error: {e}")
        return get_file_history()

def get_suggestions(text, max_suggestions=10):
    """Get completion suggestions for a partial command"""
    options = []

    # Get available commands from kernel
    try:
        from core.utils.kernel import command_kernel
        available_commands = list(command_kernel.available_commands.keys())
    except:
        # Fallback to basic commands
        available_commands = [
            'help', 'commands', 'cpu', 'mem', 'ps', 'disk', 'network', 'sysinfo', 'uptime',
            'pwd', 'ls', 'cd', 'clear', 'exit', 'history', 'suggest'
        ]

    # Add common external commands
    available_commands.extend(['python', 'pip', 'git', 'node', 'npm', 'curl', 'ping'])

    # Database-based history completion (prioritize recent commands)
    db_history = get_db_history(50)  # Get last 50 commands
    options.extend([h for h in db_history if h.startswith(text)])

    # Command completion
    options.extend([cmd for cmd in available_commands if cmd.startswith(text)])

    # File completion
    options.extend(glob.glob(text + '*'))

    # Remove duplicates while preserving order (recent history first)
    seen = set()
    unique_options = []
    for option in options:
        if option not in seen:
            seen.add(option)
            unique_options.append(option)

    return unique_options[:max_suggestions]

def completer(text, state):
    """Readline completer function"""
    if state == 0:
        completer.matches = get_suggestions(text)
    try:
        return completer.matches[state]
    except IndexError:
        return None

if READLINE_AVAILABLE:
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    if os.path.exists(HIST_FILE):
        readline.read_history_file(HIST_FILE)

def send_to_daemon(cmd):
    try:
        if SOCKET_TYPE == "tcp":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(cmd.encode())
                return s.recv(4096).decode()
        else:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.connect(SOCKET_PATH)
                s.sendall(cmd.encode())
                return s.recv(4096).decode()
    except ConnectionRefusedError:
        return "Error: Daemon not running. Start with 'python main.py daemon'"
    except Exception as e:
        return f"Connection error: {e}"

def main():
    print("AI-Augmented Command Terminal")
    print("Type 'exit' to quit, 'history' to view command history")
    if not READLINE_AVAILABLE:
        print("💡 Type 'suggest <partial>' for command suggestions")
    while True:
        try:
            cmd = input("ai-os> ")
            if cmd.strip() == "exit":
                break
            if cmd.strip() == "history":
                # Show database history
                db_history = get_db_history(20)
                if db_history:
                    for i, h in enumerate(db_history, 1):
                        print(f"{i}: {h}")
                else:
                    print("No command history available")
                continue
            if cmd.strip().startswith("suggest "):
                # Manual suggestion command for systems without readline
                partial = cmd.strip()[8:].strip()  # Remove "suggest " prefix
                if partial:
                    suggestions = get_suggestions(partial)
                    if suggestions:
                        print("💡 Suggestions:")
                        for i, suggestion in enumerate(suggestions, 1):
                            print(f"  {i}. {suggestion}")
                    else:
                        print("💡 No suggestions found")
                else:
                    print("💡 Usage: suggest <partial_command>")
                continue
            response = send_to_daemon(cmd)
            print(response)
            # History is now stored by the daemon in the database
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
