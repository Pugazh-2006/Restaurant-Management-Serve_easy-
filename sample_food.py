import sqlite3
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM menu_items")
menu_data = [
    ("Masala Dosa", 60, "masala_dosa.jpg"),
    ("Panner Butter Masala", 150, "panner_masala.jpg"),
    ("Chicken Biriyani", 180, "biriyani.jpg"),
    ("Idli Sambar", 40, "idly.jpg")
]

cursor.executemany("INSERT INTO menu_items (name, price, image) VALUES (?, ?, ?)", menu_data)
conn.commit()
conn.close()
