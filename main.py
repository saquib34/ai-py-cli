# AI Terminal Entry Point

import sys
import os
import argparse

def check_requirements():
    """Check if basic requirements are met"""
    try:
        # readline is Unix-only, optional on Windows
        try:
            import readline
        except ImportError:
            if os.name != 'nt':  # Not Windows, readline should be available
                print("⚠️  readline not available (install with: pip install readline)")
            # On Windows, readline is not needed

        import psutil
        import sqlite3
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Install with: pip install -r requirements.txt")
        return False
    return True

def run_legacy_terminal():
    """Run the legacy terminal system (CLI + Daemon)"""
    if not check_requirements():
        sys.exit(1)

    if len(sys.argv) > 2 and sys.argv[2] == "daemon":
        print("🚀 Starting Legacy AI Terminal Daemon...")
        try:
            from terminal.daemon.daemon import run_daemon
            run_daemon()
        except KeyboardInterrupt:
            print("\n👋 Daemon stopped")
        except Exception as e:
            print(f"❌ Daemon error: {e}")
            sys.exit(1)
    else:
        print("💻 Starting Legacy AI Terminal CLI...")
        print("Tip: Start daemon first with 'python main.py daemon'")
        try:
            from terminal.cli.cli import main as cli_main
            cli_main()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        except Exception as e:
            print(f"❌ CLI error: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='AI Terminal - Simple CLI + Daemon')
    parser.add_argument('subcommand', nargs='?', choices=['daemon'], help='Start daemon mode')

    args = parser.parse_args()

    if args.subcommand == 'daemon':
        print("🚀 Starting AI Terminal Daemon...")
        try:
            from terminal.daemon.daemon import run_daemon
            run_daemon()
        except KeyboardInterrupt:
            print("\n👋 Daemon stopped")
        except Exception as e:
            print(f"❌ Daemon error: {e}")
            sys.exit(1)
    else:
        print("💻 Starting AI Terminal CLI...")
        print("Tip: Start daemon first with 'python main.py daemon'")
        try:
            from terminal.cli.cli import main as cli_main
            cli_main()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        except Exception as e:
            print(f"❌ CLI error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()