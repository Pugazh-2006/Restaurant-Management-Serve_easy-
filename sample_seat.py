import sqlite3

conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

seat_data = [("A1",), ("A2",), ("B1",), ("B2",)]

cursor.executemany("INSERT INTO seats (seat_number) VALUES (?)", seat_data)

conn.commit()
conn.close()