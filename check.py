import sqlite3
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM seats")
print(cursor.fetchall())
conn.close()