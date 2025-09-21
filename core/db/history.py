import sqlite3
import os
from datetime import datetime

def init_db(db_path):
    """Initialize database with user-specific history support"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Legacy table for backward compatibility
    cur.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, cmd TEXT)")

    # New user-specific history table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            command TEXT NOT NULL,
            result TEXT,
            executed_at TEXT NOT NULL,
            success BOOLEAN,
            execution_time REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    # Create indexes for better performance
    cur.execute("CREATE INDEX IF NOT EXISTS idx_user_history ON user_history(user_id, executed_at DESC)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_command_time ON user_history(executed_at DESC)")

    conn.commit()
    return conn

def store_command(conn, cmd, user_id=None, result=None, success=None, execution_time=None):
    """Store command in history (supports both legacy and user-specific)"""
    cur = conn.cursor()

    if user_id is not None:
        # Store in user-specific history
        cur.execute("""
            INSERT INTO user_history (user_id, command, result, executed_at, success, execution_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            cmd,
            result,
            datetime.utcnow().isoformat(),
            success,
            execution_time
        ))
    else:
        # Store in legacy history for backward compatibility
        cur.execute("INSERT INTO history (cmd) VALUES (?)", (cmd,))

    conn.commit()

def get_history(conn, user_id=None, limit=50):
    """Get command history (supports both legacy and user-specific)"""
    cur = conn.cursor()

    if user_id is not None:
        # Get user-specific history
        cur.execute("""
            SELECT command, executed_at, result, success, execution_time
            FROM user_history
            WHERE user_id = ?
            ORDER BY executed_at DESC
            LIMIT ?
        """, (user_id, limit))

        history = []
        for row in cur.fetchall():
            history.append({
                'command': row[0],
                'executed_at': row[1],
                'result': row[2],
                'success': bool(row[3]) if row[3] is not None else None,
                'execution_time': row[4]
            })
        return history
    else:
        # Get legacy history
        cur.execute("SELECT cmd FROM history ORDER BY id DESC LIMIT ?", (limit,))
        return [{'command': row[0]} for row in cur.fetchall()]

def migrate_legacy_history(conn, user_id):
    """Migrate legacy history to user-specific history"""
    cur = conn.cursor()

    # Get all legacy commands
    cur.execute("SELECT cmd FROM history ORDER BY id")
    legacy_commands = cur.fetchall()

    # Insert into user history
    for cmd_row in legacy_commands:
        cur.execute("""
            INSERT INTO user_history (user_id, command, executed_at)
            VALUES (?, ?, ?)
        """, (
            user_id,
            cmd_row[0],
            datetime.utcnow().isoformat()  # Use current time for migrated commands
        ))

    conn.commit()

    # Optionally clear legacy table
    # cur.execute("DELETE FROM history")
    # conn.commit()

def get_user_stats(conn, user_id):
    """Get statistics for user's command history"""
    cur = conn.cursor()

    # Total commands
    cur.execute("SELECT COUNT(*) FROM user_history WHERE user_id = ?", (user_id,))
    total_commands = cur.fetchone()[0]

    # Successful commands
    cur.execute("SELECT COUNT(*) FROM user_history WHERE user_id = ? AND success = 1", (user_id,))
    successful_commands = cur.fetchone()[0]

    # Average execution time
    cur.execute("""
        SELECT AVG(execution_time)
        FROM user_history
        WHERE user_id = ? AND execution_time IS NOT NULL
    """, (user_id,))
    avg_execution_time = cur.fetchone()[0] or 0

    return {
        'total_commands': total_commands,
        'successful_commands': successful_commands,
        'success_rate': successful_commands / total_commands if total_commands > 0 else 0,
        'avg_execution_time': avg_execution_time
    }

def search_user_history(conn, user_id, query, limit=20):
    """Search user's command history"""
    cur = conn.cursor()

    search_pattern = f"%{query}%"
    cur.execute("""
        SELECT command, executed_at, result, success
        FROM user_history
        WHERE user_id = ? AND (command LIKE ? OR result LIKE ?)
        ORDER BY executed_at DESC
        LIMIT ?
    """, (user_id, search_pattern, search_pattern, limit))

    results = []
    for row in cur.fetchall():
        results.append({
            'command': row[0],
            'executed_at': row[1],
            'result': row[2],
            'success': bool(row[3]) if row[3] is not None else None
        })

    return results
