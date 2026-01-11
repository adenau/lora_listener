import sys
import sqlite3

class Database:
    """Handles all SQLite database operations for LoRa messages."""
    
    def __init__(self, db_file="messages.db"):
        """Initialize database with specified file path."""
        self.db_file = db_file
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database and create messages table if it doesn't exist."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    message TEXT NOT NULL
                )
            ''')
            conn.commit()
    
    def log_message(self, message: str, timestamp: str):
        """Log message with timestamp to SQLite database."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO messages (timestamp, message) VALUES (?, ?)',
                    (timestamp, message)
                )
                conn.commit()
        except Exception as e:
            print(f"Database error: {e}", file=sys.stderr)
    
    def get_last_messages(self, limit: int = 100):
        """Retrieve the last N messages from the database."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.row_factory = sqlite3.Row  # Return rows as dictionaries
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT id, timestamp, message FROM messages ORDER BY id DESC LIMIT ?',
                    (limit,)
                )
                rows = cursor.fetchall()
                # Convert to list of dictionaries
                return [dict(row) for row in rows]
        except Exception as e:
            print(f"Database error: {e}", file=sys.stderr)
            return []
