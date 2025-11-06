import sqlite3
from datetime import datetime

conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# Step 1: Add column
cursor.execute("ALTER TABLE orders ADD COLUMN order_date TEXT")
print("Column added")

# Step 2: Update existing rows
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cursor.execute("UPDATE orders SET order_date = ?", (now,))
conn.commit()
print("Existing rows updated")

conn.close()