import sqlite3

conn = sqlite3.connect('restaurant.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL,
               password TEXT NOT NULL,
               email TEXT NOT NULL)''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS menu_items (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               price REAL NOT NULL,
               image TEXT,
               description TEXT,
               type TEXT,
               category TEXT)''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS seats (
               seat_id INTEGER PRIMARY KEY,
               status TEXT DEFAULT 'available',
               user_id INTEGER,
               FOREIGN KEY(user_id) REFERENCES users(id)
               )''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS orders (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER,
               seat_id INTEGER,
               total REAL,
               status TEXT,
               created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY(user_id) REFERENCES users(id),
               FOREIGN KEY(seat_id) REFERENCES seats(id)
               )
               ''')
conn.commit()
conn.close()
