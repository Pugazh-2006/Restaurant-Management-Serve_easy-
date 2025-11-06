import sqlite3

# Connect to your database
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# Enable foreign key enforcement
cursor.execute("PRAGMA foreign_keys = ON")

# 🔥 Drop the existing orders table
cursor.execute("DROP TABLE IF EXISTS orders")
print("✅ Dropped old 'orders' table")

# ✅ Recreate orders table with correct foreign keys
cursor.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    seat_id INTEGER,
    total REAL,
    status TEXT,
    timestamp TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(seat_id) REFERENCES seats(seat_id)
)
""")
print("✅ Recreated 'orders' table with correct foreign keys")

# Commit and close
conn.commit()
conn.close()
print("✅ Migration complete")