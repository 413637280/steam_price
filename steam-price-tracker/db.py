import sqlite3

def init_db():
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_name TEXT,
        price REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tracked_games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_name TEXT UNIQUE
    )
    """)
    conn.commit()
    conn.close()

def insert_price(game_name, price):
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO price_history (game_name, price) VALUES (?, ?)",
        (game_name, float(price))
    )
    conn.commit()
    conn.close()

def get_prices(game_name):
    conn = sqlite3.connect("prices.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT price, timestamp FROM price_history WHERE game_name = ? ORDER BY timestamp",
        (game_name,)
    )
    rows = cursor.fetchall()
    conn.close()
    data = []
    for row in rows:
        data.append({
            "price": row["price"],
            "timestamp": row["timestamp"]
        })
    return data

def add_tracked_game(game_name):
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO tracked_games (game_name) VALUES (?)",
            (game_name,)
        )
        conn.commit()
    except Exception as e:
        print(f"Add tracked game error: {e}")
    finally:
        conn.close()
