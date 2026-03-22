import sqlite3

def get_connection():
    return sqlite3.connect("travel.db")


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS travel (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        location TEXT,
        type TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_data(text, location, type_):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO travel (text, location, type) VALUES (?, ?, ?)",
        (text, location, type_)
    )

    conn.commit()
    conn.close()


def get_data(location=None, type_=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT text FROM travel WHERE 1=1"
    params = []

    if location:
        query += " AND location=?"
        params.append(location)

    if type_:
        query += " AND type=?"
        params.append(type_)

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()

    return [r[0] for r in results]