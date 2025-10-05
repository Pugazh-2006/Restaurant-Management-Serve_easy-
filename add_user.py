import sqlite3
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "1234"))
conn.commit()
conn.close()
