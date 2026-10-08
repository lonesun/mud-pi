import sqlite3
from contextlib import closing

SCHEMA = "dta/players/schema.sql"
DEFAULT_DB = "dta/players/roster.db"

def seed_database(database_file=DEFAULT_DB, schema_file=SCHEMA):
    with closing(sqlite3.connect(database_file)) as conn:
        with open(schema_file, "r") as f:
            conn.executescript(f.read())

def attempt_load(username, database_file=DEFAULT_DB, expected_field=""):
    print(f"Attempting to load data for user: {username}")
    with closing(sqlite3.connect(database_file)) as conn:
        if expected_field in ["current_room", "description"]:
            result = conn.execute(
                f"SELECT {expected_field} FROM roster WHERE name = ?",
                (username,),
            ).fetchone()
        return result[0] if result else None  # None for a new player

def save_user_data(username, value, database_file=DEFAULT_DB, expected_field=""):
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
