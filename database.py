import sqlite3
from datetime import date
from typing import Optional

DB_PATH = "promptmaster.db"


class Database:
    def __init__(self):
        self._init_db()

    def _conn(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    plan TEXT DEFAULT 'free',
                    language TEXT DEFAULT 'en',
                    created_at TEXT DEFAULT (date('now'))
                );

                CREATE TABLE IF NOT EXISTS usage (
                    user_id INTEGER,
                    date TEXT,
                    count INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, date)
                );

                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    topic TEXT,
                    ai_platform TEXT,
                    mode TEXT,
                    prompt_text TEXT,
                    created_at TEXT DEFAULT (datetime('now'))
                );
            """)

    def ensure_user(self, user_id: int, username: str):
        with self._conn() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)",
                (user_id, username)
            )

    def get_plan(self, user_id: int) -> str:
        with self._conn() as conn:
            row = conn.execute("SELECT plan FROM users WHERE id=?", (user_id,)).fetchone()
            return row["plan"] if row else "free"

    def set_plan(self, user_id: int, plan: str):
        with self._conn() as conn:
            conn.execute("UPDATE users SET plan=? WHERE id=?", (plan, user_id))

    def get_language(self, user_id: int) -> str:
        with self._conn() as conn:
            row = conn.execute("SELECT language FROM users WHERE id=?", (user_id,)).fetchone()
            return row["language"] if row else "en"

    def set_language(self, user_id: int, lang: str):
        with self._conn() as conn:
            conn.execute("UPDATE users SET language=? WHERE id=?", (lang, user_id))

    def get_daily_usage(self, user_id: int) -> int:
        today = str(date.today())
        with self._conn() as conn:
            row = conn.execute(
                "SELECT count FROM usage WHERE user_id=? AND date=?",
                (user_id, today)
            ).fetchone()
            return row["count"] if row else 0

    def increment_usage(self, user_id: int):
        today = str(date.today())
        with self._conn() as conn:
            conn.execute("""
                INSERT INTO usage (user_id, date, count) VALUES (?, ?, 1)
                ON CONFLICT(user_id, date) DO UPDATE SET count = count + 1
            """, (user_id, today))

    def save_prompt(self, user_id: int, topic: str, ai: str, mode: str, text: str):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO prompts (user_id, topic, ai_platform, mode, prompt_text) VALUES (?,?,?,?,?)",
                (user_id, topic, ai, mode, text)
            )

    def get_history(self, user_id: int, limit: int = 5):
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT topic, ai_platform, mode, created_at FROM prompts WHERE user_id=? ORDER BY id DESC LIMIT ?",
                (user_id, limit)
            ).fetchall()
            return [dict(r) for r in rows]

    def get_total_prompts(self, user_id: int) -> int:
        with self._conn() as conn:
            row = conn.execute("SELECT COUNT(*) as c FROM prompts WHERE user_id=?", (user_id,)).fetchone()
            return row["c"] if row else 0

    def get_total_users(self) -> int:
        with self._conn() as conn:
            row = conn.execute("SELECT COUNT(*) as c FROM users").fetchone()
            return row["c"] if row else 0
