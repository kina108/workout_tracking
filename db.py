import sqlite3

DB = "simple_workout_pin.db"


def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)


def init_db(conn: sqlite3.Connection):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
      user TEXT PRIMARY KEY,
      pin  TEXT NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user TEXT NOT NULL,
      day  TEXT NOT NULL,
      exercise TEXT NOT NULL,
      weight REAL NOT NULL,
      reps INTEGER NOT NULL,
      FOREIGN KEY(user) REFERENCES users(user)
    )
    """)
    conn.commit()


def sign_in_or_create(conn: sqlite3.Connection, user, pin) :
    row = conn.execute("SELECT pin FROM users WHERE user=?", (user,)).fetchone()
    if row is None:
        conn.execute("INSERT INTO users(user, pin) VALUES (?, ?)", (user, pin))
        conn.commit()
        return True
    return row[0] == pin


def add_log(conn: sqlite3.Connection, user, day, exercise, weight, reps):
    conn.execute(
        "INSERT INTO logs(user, day, exercise, weight, reps) VALUES (?, ?, ?, ?, ?)",
        (user, day, exercise, float(weight), int(reps)),
    )
    conn.commit()


def get_recent_logs(conn: sqlite3.Connection, user, limit: int = 50):
    return conn.execute(
        """
        SELECT id, day, exercise, weight, reps
        FROM logs
        WHERE user=?
        ORDER BY day DESC, id DESC
        LIMIT ?
        """,
        (user, limit),
    ).fetchall()


def delete_log(conn: sqlite3.Connection, user, log_id):
    conn.execute("DELETE FROM logs WHERE user=? AND id=?", (user, int(log_id)))
    conn.commit()


def list_exercises(conn: sqlite3.Connection, user):
    rows = conn.execute(
        "SELECT DISTINCT exercise FROM logs WHERE user=? ORDER BY exercise",
        (user,),
    ).fetchall()
    return [r[0] for r in rows]


def get_logs_by_exercise(conn: sqlite3.Connection, user, exercise):
    return conn.execute(
        """
        SELECT id, day, weight, reps
        FROM logs
        WHERE user=? AND exercise=?
        ORDER BY day ASC, id ASC
        """,
        (user, exercise),
    ).fetchall()


def list_dates(conn: sqlite3.Connection, user):
    rows = conn.execute(
        "SELECT DISTINCT day FROM logs WHERE user=? ORDER BY day DESC",
        (user,),
    ).fetchall()
    return [r[0] for r in rows]


def get_logs_by_date(conn: sqlite3.Connection, user, day):
    return conn.execute(
        """
        SELECT id, exercise, weight, reps
        FROM logs
        WHERE user=? AND day=?
        ORDER BY exercise ASC, id ASC
        """,
        (user, day),
    ).fetchall()


