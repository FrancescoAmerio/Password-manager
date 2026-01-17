import os
import sqlite3
from pathlib import Path
from typing import Optional, Any

class DatabaseConnection:
    def __init__(self, db_path: str | None = None) -> None:
        if db_path is None:
            appdata = os.environ.get("APPDATA", str(Path.home()))
            app_dir = Path(appdata) / "PasswordManager"
            app_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(app_dir / "passwords.db")

        self.db_path = db_path
        self.conn: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    def open(self) -> None:
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        # PRAGMA utili
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.cursor.execute("PRAGMA journal_mode = WAL;")

        self._init_schema()
        self.conn.commit()

        print(f"SQLite DB opened: {self.db_path}")

    def _init_schema(self) -> None:
        assert self.conn is not None and self.cursor is not None

        # users
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                salt BLOB NOT NULL
            );
        """)

        # user_credentials
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                service TEXT NOT NULL,
                password TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id, service)
            );
        """)

        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_credentials_user_id
            ON user_credentials(user_id);
        """)
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_credentials_service
            ON user_credentials(service);
        """)

    def execute_query(
        self,
        query: str,
        params: Optional[tuple[Any, ...]] = None,
        *,
        fetch: bool = True,
        commit: bool = False
    ) -> Optional[list[Any]]:
        if self.conn is None or self.cursor is None:
            print("Connection is not active.")
            return None

        try:
            self.cursor.execute(query, params or ())
            if commit:
                self.conn.commit()
            if fetch:
                return self.cursor.fetchall()
            return []
        except sqlite3.Error as e:
            print("Error while executing query:", e)
            return None

    def close(self) -> None:
        try:
            if self.cursor is not None:
                self.cursor.close()
                self.cursor = None
            if self.conn is not None:
                self.conn.close()
                self.conn = None
            print("Connection closed.")
        except Exception:
            pass
