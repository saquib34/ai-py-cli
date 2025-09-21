import socket
import subprocess
import sqlite3
import os
import sys

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))

from core.db.history import init_db, store_command
from core.ai.gemini import ai_process_command, needs_confirmation
from core.utils.kernel import command_kernel

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

DB_PATH = "history.db"



# Global command kernel instance
command_kernel = None

def execute_command(cmd):
    """
    Execute command using the intelligent kernel with AI fallback
    """
    global command_kernel
    if command_kernel is None:
        from core.utils.kernel import command_kernel as kernel
        command_kernel = kernel

    if not cmd.strip():
        return ""

    # First try the kernel's intelligent execution
    output, success = command_kernel.execute_command(cmd)

    if success:
        return output
    else:
        # If kernel fails, try AI interpretation as fallback
        try:
            safe_cmd, risk = ai_process_command(cmd)
            if risk and needs_confirmation(safe_cmd):
                # For risky commands, return the suggestion but don't execute
                return f"⚠️  Risky command detected: {safe_cmd}\nUse confirmation in CLI for dangerous operations"
            else:
                # Try executing the AI-interpreted command
                result, ai_success = command_kernel.execute_command(safe_cmd)
                if ai_success:
                    return f"🤖 AI interpreted '{cmd}' as: {safe_cmd}\n{result}"
                else:
                    return f"❌ Command failed: {result}"
        except Exception as e:
            return f"❌ AI processing failed: {e}\nOriginal error: {output}"

def run_daemon():
    print("Starting daemon initialization...")
    if SOCKET_TYPE == "tcp":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
    else:
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)
        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_socket.bind(SOCKET_PATH)

    print("Initializing database...")
    conn = init_db(DB_PATH)
    print("Database initialized successfully")
    server_socket.listen()
    print(f"Daemon running on {SOCKET_TYPE} socket...")

    try:
        while True:
            print("Waiting for client connection...")
            client, addr = server_socket.accept()
            print(f"Client connected: {addr}")
            try:
                with client:
                    data = client.recv(4096).decode()
                    print(f"Received data: '{data}'")
                    if not data:
                        continue

                    # AI processing
                    print("Processing with AI...")
                    safe_cmd, risk = ai_process_command(data)
                    print(f"AI result: '{safe_cmd}', risk: {risk}")
                    if risk and needs_confirmation(safe_cmd):
                        # Send confirmation prompt
                        confirm_msg = f"[AI] Interpreted: {safe_cmd}\nExecute? [y/N]: "
                        client.sendall(confirm_msg.encode())

                        # Wait for confirmation response
                        try:
                            confirm_data = client.recv(4096).decode().strip().lower()
                            if confirm_data not in ['y', 'yes']:
                                client.sendall(b"Aborted by user.\n")
                                continue
                        except:
                            client.sendall(b"Confirmation timeout. Aborted.\n")
                            continue

                    # Store in history
                    print("Storing command in history...")
                    store_command(conn, data)
                    # Execute
                    print("Executing command...")
                    output = execute_command(safe_cmd)
                    print(f"Command output length: {len(output)}")
                    client.sendall(output.encode())
            except Exception as client_error:
                print(f"Error handling client: {client_error}")
                import traceback
                traceback.print_exc()
                try:
                    client.sendall(f"Server error: {client_error}".encode())
                except:
                    pass  # Client might already be disconnected
    except KeyboardInterrupt:
        print("Daemon shutting down...")
    except Exception as e:
        print(f"Daemon error: {e}")
        import traceback
        traceback.print_exc()
    except KeyboardInterrupt:
        print("Daemon shutting down...")
    except Exception as e:
        print(f"Daemon error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        server_socket.close()
        if SOCKET_TYPE == "unix":
            os.remove(SOCKET_PATH)

if __name__ == "__main__":
    run_daemon()
