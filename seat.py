import sqlite3

conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

for seat_id in range(1, 21):
    cursor.execute("INSERT OR IGNORE INTO seats (seat_id, status) VALUES (?, ?)", (seat_id, 'available'))

conn.commit()
conn.close()
print("Seats preloaded successfully.")
