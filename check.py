import sqlite3

# Connect to the database
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()

# Execute the query to fetch deleted items
cursor.execute("SELECT id, name FROM menu_items WHERE status = 'deleted'")
deleted_items = cursor.fetchall()

# Print the results
print("🗑️ Deleted Menu Items:")
for item in deleted_items:
    print(f"ID: {item[0]}, Name: {item[1]}")

# Close the connection
conn.close()