from dbconn import*

cursor.execute("""
    CREATE TABLE IF NOT EXISTS rides (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        pickup_lat REAL,
        pickup_lon REAL,
        drop_lat REAL,
        drop_lon REAL,
        time TEXT,
        seats INTEGER,
        fare INTEGER
    )
""")

conn.commit()