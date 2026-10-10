import sqlite3
from contextlib import closing

SCHEMA = "dta/players/schema.sql"
DEFAULT_DB = "dta/players/roster.db"
PLAYER_FIELDS = ("current_room", "description") # todo: add score fields

def _check_field(expected_field):
    if expected_field not in PLAYER_FIELDS:
        raise ValueError(f"Unsupported roster field: {expected_field!r}")

def seed_database(database_file=DEFAULT_DB, schema_file=SCHEMA):
    with closing(sqlite3.connect(database_file)) as conn:
        # Leave an existing roster untouched; the schema would fail to re-create it.
        exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'roster'"
        ).fetchone()
        if exists:
            return
        with open(schema_file, "r") as f:
            conn.executescript(f.read())

def attempt_load(username, database_file=DEFAULT_DB, expected_field=""):
    _check_field(expected_field)
    print(f"Attempting to load data for user: {username}")
    with closing(sqlite3.connect(database_file)) as conn:
        result = conn.execute(
            f"SELECT {expected_field} FROM roster WHERE name = ?",
            (username,),
        ).fetchone()
    return result[0] if result else None  # None for a new player

def save_user_data(username, value, database_file=DEFAULT_DB, expected_field=""):
    _check_field(expected_field)
    with closing(sqlite3.connect(database_file)) as conn:
        with conn:  # commits on success, rolls back on error
            cur = conn.execute(
                f"UPDATE roster SET {expected_field} = ? WHERE name = ?",
                (value, username),
            )
            if cur.rowcount == 0:
                conn.execute(
                    f"INSERT INTO roster (name, {expected_field}) VALUES (?, ?)",
                    (username, value),
                )
            print(f"Saved data for user: {username}, field: {expected_field}, value: {value}")
