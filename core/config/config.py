# AI Terminal Core Configuration
# Legacy terminal and shared settings

import os

# Legacy Terminal Network settings (for backward compatibility)
LEGACY_HOST = "127.0.0.1"
LEGACY_PORT = 65432

# Database settings (legacy path)
DB_PATH = "history.db"

# AI settings (shared with backend)
GEMINI_MODEL = "gemini-1.5-flash"
MAX_RETRIES = 3
TIMEOUT = 30  # seconds

# Safety settings (used by AI processing)
RISKY_PATTERNS = [
    "rm -rf", "rm -r", "del /f /s", "format", "fdisk", "dd if=",
    "mkfs", "sudo", "su", "chmod 777", "chown root", "passwd",
    "shutdown", "reboot", "halt", "poweroff"
]

# History settings (legacy terminal)
MAX_HISTORY_SIZE = 1000
HISTORY_FILE = "~/.aios_history"