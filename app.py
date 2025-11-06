from flask import Flask, render_template,request,redirect, send_file,session
import os
import re
import sqlite3
import openpyxl
from io import BytesIO
BASE = os.path.join(os.path.dirname(__file__), 'Restaurant-Management-Serve_easy-')
from flask_caching import Cache 
from datetime import datetime, timedelta

app = Flask(
    __name__,
    static_folder=os.path.join(BASE, 'static'),
    template_folder=os.path.join(BASE, 'templates'),
)
# Use a strong secret key for production
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')
cache = Cache(app, config={'CACHE_TYPE':'simple'})

def init_db():
    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            role TEXT DEFAULT 'user'
        )
        ''')
        
        # Check if admin user exists, if not create one
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute('''
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
            ''', ('admin', 'admin123', 'admin'))
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
    finally:
        conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def home():
    if 'username' in session and 'role' in session:
        if session.get('role') == 'admin':
            return redirect('/admin')
        return redirect('/menu')
    return render_template('landing.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to appropriate page
    if 'username' in session:
        if session.get('role') == 'admin':
            return redirect('/admin')
        return redirect('/menu')

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            message = "Please fill in all fields"
            return render_template('login.html', message=message)

        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            
            if user:
                # Store user info in session
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['role'] = user[4]
                
                # Redirect based on role
                if user[4] == 'admin':
                    return redirect('/admin')
                return redirect('/menu')
            else:
                message = "Invalid username or password"
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            message = "An error occurred. Please try again."
        finally:
            conn.close()

    return render_template('login.html', message=message)

from datetime import datetime

@app.route('/admin')
def admin_panel():
    if session.get('username') != 'admin':
        print("⚠️ Unauthorized access attempt to admin panel")
        return redirect('/login')

    conn = sqlite3.connect('restaurant.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM menu_items WHERE status = 'active'")
    active_menu = cursor.fetchall()

    cursor.execute("SELECT * FROM menu_items WHERE status = 'deleted'")
    deleted_menu = cursor.fetchall()

    cursor.execute("SELECT * FROM seats")
    seats = cursor.fetchall()

    cursor.execute("""
        SELECT order_items.id, users.username, seats.seat_id, menu_items.name, menu_items.price, orders.id
        FROM order_items
        JOIN orders ON order_items.order_id = orders.id
        JOIN users ON orders.user_id = users.id
        JOIN seats ON orders.seat_id = seats.seat_id
        JOIN menu_items ON order_items.item_id = menu_items.id
        WHERE orders.status = 'pending'
    """)
    pending_orders = cursor.fetchall()
    print("✅ Pending orders fetched:", len(pending_orders))

    today = datetime.now().date()
    cursor.execute("""
        SELECT menu_items.name, COUNT(*) AS count
        FROM (
            SELECT item_id FROM order_items
            JOIN orders ON order_items.order_id = orders.id
            WHERE DATE(orders.timestamp) = ?
            UNION ALL
            SELECT item_id FROM served_items
            JOIN orders ON served_items.order_id = orders.id
            WHERE DATE(orders.timestamp) = ?
        ) AS all_items
        JOIN menu_items ON all_items.item_id = menu_items.id
        GROUP BY menu_items.name
        ORDER BY count DESC
    """, (today, today))
    dish_counts = cursor.fetchall()
    print("✅ Dish counts fetched:", len(dish_counts))

    cursor.execute("""
        SELECT SUM(menu_items.price)
        FROM (
            SELECT item_id FROM order_items
            JOIN orders ON order_items.order_id = orders.id
            WHERE DATE(orders.timestamp) = ?
            UNION ALL
            SELECT item_id FROM served_items
            JOIN orders ON served_items.order_id = orders.id
            WHERE DATE(orders.timestamp) = ?
        ) AS all_items
        JOIN menu_items ON all_items.item_id = menu_items.id
    """, (today, today))
    total_revenue = cursor.fetchone()[0] or 0

    conn.close()

    return render_template('admin.html',
                           active_menu=active_menu,
                           deleted_menu=deleted_menu,
                           seats=seats,
                           pending_orders=pending_orders,
                           dish_counts=dish_counts,
                           total_revenue=total_revenue)

@app.route('/free_seat', methods=['POST'])
def free_seat():
    seat_id = request.form['seat_id']
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE seats SET status='available', user_id=NULL WHERE seat_id=?", (seat_id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    price = request.form['price']
    description = request.form['description']
    image = request.form['image']
    type_ = request.form['type']
    category = request.form['category']

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO menu_items (name, price, description, image, type, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, price, description, image, type_, category))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/admin_reserve_seat', methods=['POST'])
def admin_reserve_seat():
    seat_id = request.form['seat_id']
    username = request.form['username']

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        cursor.execute("UPDATE seats SET status='reserved', user_id=? WHERE seat_id=?", (user_id, seat_id))
        conn.commit()

    conn.close()
    return redirect('/admin')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        def is_valid_password(pwd):
            return (
                len(pwd) >= 8 and
                re.search(r'[A-Z]', pwd) and
                re.search(r'[a-z]', pwd) and
                re.search(r'[0-9]', pwd)
            )

        if not is_valid_password(password):
            error = "Password must be at least 8 characters long and include one uppercase letter, one lowercase letter, and one digit."
            return render_template('register.html', error=error)

        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', error="Username already exists. Try a different one.")

        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        conn.close()
        return render_template('login.html', message="Registration Successful! Please Login.")

    return render_template('register.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
	if request.method == 'POST':
		email = request.form['email']

		conn = sqlite3.connect('restaurant.db')
		cursor = conn.cursor()
		cursor.execute("SELECT username,password FROM users WHERE email=?", (email,))
		user = cursor.fetchone()
		conn.close()

		if user:
			return f"Your username is {user[0]} and Your password is {user[1]}"
		else:
			return "No account found with that email."
	return render_template('forgot.html')

@app.route('/menu')
def menu():
    if 'user_id' not in session:
        return redirect('/')

    food_type = request.args.get('type')
    category = request.args.get('category')
    user_id = session['user_id']

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    query = """
        SELECT id, name, price, image, description
        FROM menu_items
        WHERE status = 'active'
    """
    params = []

    if food_type:
        query += " AND type = ?"
        params.append(food_type)
    if category:
        query += " AND category = ?"
        params.append(category)

    query += " LIMIT 1000"
    cursor.execute(query, params)

    items = []
    for row in cursor.fetchall():
        image = row[3].strip() if row[3] and row[3].strip() else 'masala_dosa.webp'
        description = row[4] if len(row) > 4 else ''
        items.append((row[0], row[1], row[2], image, description))

    cursor.execute("SELECT seat_id FROM seats WHERE user_id=? AND status='reserved'", (user_id,))
    seat = cursor.fetchone()

    cart = session.get('cart', {})
    cart_items = []
    total = 0
    for item_id, quantity in cart.items():
        cursor.execute("SELECT name, price FROM menu_items WHERE id=? AND status='active'", (item_id,))
        item = cursor.fetchone()
        if item:
            cart_items.append((item[0], item[1]))
            total += item[1] * quantity

    conn.close()

    return render_template('menu.html',
                           items=items,
                           selected_type=food_type,
                           selected_category=category,
                           seat=seat,
                           cart_items=cart_items,
                           total=total)

@app.route('/restore_menu_item', methods=['POST'])
def restore_menu_item():
    if session.get('username') != 'admin':
        return redirect('/login')  

    item_id = request.form.get('item_id')

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE menu_items SET status = 'active' WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    
    return redirect('/admin#deleted')  

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
	item_id = request.form['item_id']
	if 'cart' not in session:
		session['cart'] = {}
	cart = session['cart']
	cart[item_id] = cart.get(item_id, 0) + 1
	session['cart'] = cart
	return redirect('/menu')

@app.route('/cart')
def cart():
	if 'cart' not in session or not session['cart']:
		return render_template('cart.html',items=[], total=0)
	
	conn = sqlite3.connect('restaurant.db')
	cursor = conn.cursor()

	cart_items = []
	total = 0

	for item_id, quantity in session['cart'].items():
		item_id = tuple(map(int, session['cart'].keys()))
		cursor.execute(f"SELECT id, name, price, image FROM menu_items WHERE id IN ({','.join(['?']*len(item_id))})", item_id)
		item = cursor.fetchone()
		if item:
			subtotal = item[2] * quantity 
			total += subtotal
			cart_items.append({
				'id' : item[0],
				'name' : item[1],
				'price' : item[2],
				'image': item[3],
				'quantity': quantity,
				'subtotal': subtotal
			})
	conn.close()
	return render_template('cart.html', items=cart_items, total=total)

@app.route('/update_cart', methods=['POST'])
def update_cart():
	item_id = request.form['item_id'].strip()
	action = request.form['action']

	if'cart' in session and item_id in session['cart']:
		if action == 'increase':
			session['cart'][item_id] += 1
		elif action == 'decrease':
			session['cart'][item_id] -=1
			if session['cart'][item_id] <= 0:
				del session['cart'][item_id]
		session.modified = True

	return redirect('/cart')

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
	item_id = request.form['item_id'].strip()
	if 'cart' in session and item_id in session['cart']:
			del session['cart'][item_id]
			session.modified = True
	return redirect('/cart')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')
@cache.cached(timeout=60)
@app.route('/reserve_seat', methods=["GET"])
def show_seats():
	conn = sqlite3.connect('restaurant.db')
	cursor = conn.cursor()
	cursor.execute("SELECT seat_id, status FROM seats")
	seats = [{'seat_id': row[0], 'status': row[1]} for row in cursor.fetchall()]
	conn.close()
	return render_template('reserve_seat.html', seats=seats)

@app.route('/reserve_seat', methods=['POST'])
def reserve_seats():
    seat_id = request.form.get('seat_id')
    user_id = session.get('user_id')

    if not seat_id:
        return "No seat selected. Please go back and choose a seat."

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM seats WHERE seat_id = ?", (seat_id,))
    status = cursor.fetchone()

    if status and status[0] == 'available':
        cursor.execute("UPDATE seats SET status = 'reserved', user_id = ? WHERE seat_id = ?", (user_id, seat_id))
        conn.commit()
        conn.close()
        return redirect('/order_summary')
    else:
        conn.close()
        return "Seat is already reserved. Please choose another seat."
@app.route('/order_summary')
def order_summary():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    user_id = session['user_id']

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()


    cursor.execute("SELECT seat_id FROM seats WHERE user_id=? AND status='reserved'", (user_id,))
    seat = cursor.fetchone()

    cart = session.get('cart', {}) 
    items = []
    total = 0

    for item_id in cart:
        cursor.execute("SELECT name, price FROM menu_items WHERE id=?", (item_id,))
        item = cursor.fetchone()
        if item:
            items.append(item)
            total += item[1]

    conn.close()

    return render_template('order_summary.html', username=username, seat=seat, items=items, total=total)

from flask import session, redirect, request
import sqlite3
from datetime import datetime

@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    user_id = session.get('user_id')
    cart = session.get('cart', {})  

    if not user_id or not cart:
        print("❌ Missing user or cart")
        return redirect('/menu')

    conn = sqlite3.connect('restaurant.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()


    cursor.execute("SELECT seat_id FROM seats WHERE user_id=? AND status='reserved'", (user_id,))
    seat = cursor.fetchone()
    seat_id = seat[0] if seat else None
    print("✅ Reserved seat:", seat_id)

    total = 0
    for item_id, qty in cart.items():
        item_id = int(item_id)
        cursor.execute("SELECT price FROM menu_items WHERE id=?", (item_id,))
        price_row = cursor.fetchone()
        if price_row:
            price = price_row[0]
            total += price * qty
        else:
            print(f"❌ Item ID {item_id} not found in menu_items")


    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO orders (user_id, seat_id, total, status, timestamp, order_date)
        VALUES (?, ?, ?, 'pending', datetime('now'), ?)
    """, (user_id, seat_id, total, order_date))
    order_id = cursor.lastrowid
    print("✅ Order created with ID:", order_id)

    for item_id, qty in cart.items():
        item_id = int(item_id)
        for _ in range(qty):
            try:
                cursor.execute("INSERT INTO order_items (order_id, item_id) VALUES (?, ?)", (order_id, item_id))
                print(f"✅ Inserted item {item_id} into order_items")
            except Exception as e:
                print(f"❌ Failed to insert item {item_id}: {e}")

    conn.commit()
    conn.close()

    
    session['cart'] = {}
    return redirect('/order_summary')

from datetime import datetime, timedelta

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    one_month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()


    cursor.execute("""
        SELECT mi.name, COUNT(*) AS total_qty, SUM(mi.price) AS total_spent
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN menu_items mi ON oi.item_id = mi.id
        WHERE o.user_id = ? AND o.order_date >= ?
        GROUP BY mi.name
        ORDER BY total_spent DESC
    """, (user_id, one_month_ago))
    dish_summary = cursor.fetchall()

    cursor.execute("""
        SELECT o.id, o.order_date, mi.name, mi.price
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN menu_items mi ON oi.item_id = mi.id
        WHERE o.user_id = ? AND o.order_date >= ?
        ORDER BY o.order_date DESC
    """, (user_id, one_month_ago))
    order_details = cursor.fetchall()

    conn.close()
    return render_template('history.html', dish_summary=dish_summary, order_details=order_details)

@app.route('/mark_served', methods=['POST'])
def mark_served():
    order_item_id = request.form['order_item_id']
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    # 🔍 Find the order ID and item ID
    cursor.execute("SELECT order_id, item_id FROM order_items WHERE id=?", (order_item_id,))
    result = cursor.fetchone()

    if result:
        order_id, item_id = result

        # ✅ Save served item to history
        cursor.execute("""
            INSERT INTO served_items (item_id, order_id)
            VALUES (?, ?)
        """, (item_id, order_id))

        # 🗑️ Delete the served item from order_items
        cursor.execute("DELETE FROM order_items WHERE id=?", (order_item_id,))
        conn.commit()

        # 🔍 Check if any items remain in the order
        cursor.execute("SELECT COUNT(*) FROM order_items WHERE order_id=?", (order_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            # ✅ Mark order as served
            cursor.execute("UPDATE orders SET status='served' WHERE id=?", (order_id,))

            # 🔍 Get the seat ID linked to this order
            cursor.execute("SELECT seat_id FROM orders WHERE id=?", (order_id,))
            seat_result = cursor.fetchone()

            if seat_result:
                seat_id = seat_result[0]

                # ✅ Free the seat
                cursor.execute("UPDATE seats SET status='available', user_id=NULL WHERE seat_id=?", (seat_id,))
                print(f"✅ Seat {seat_id} freed after serving order {order_id}")

            conn.commit()

    conn.close()
    return redirect('/admin')

from datetime import datetime, timedelta
import sqlite3
import openpyxl
from io import BytesIO

@app.route('/download_report', methods=['POST'])
def download_report():
    range_type = request.form['range']
    now = datetime.now()

    if range_type == 'today':
        start = now.date()
    elif range_type == 'week':
        start = (now - timedelta(days=7)).date()
    elif range_type == 'month':
        start = (now - timedelta(days=30)).date()

    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    # ✅ Unified query: includes both active and served items
    cursor.execute("""
        SELECT menu_items.name, COUNT(*) AS count, SUM(menu_items.price) AS total
        FROM (
            SELECT item_id FROM order_items
            JOIN orders ON order_items.order_id = orders.id
            WHERE DATE(orders.timestamp) >= ?
            UNION ALL
            SELECT item_id FROM served_items
            JOIN orders ON served_items.order_id = orders.id
            WHERE DATE(orders.timestamp) >= ?
        ) AS all_items
        JOIN menu_items ON all_items.item_id = menu_items.id
        GROUP BY menu_items.name
        ORDER BY count DESC
    """, (start, start))
    rows = cursor.fetchall()
    conn.close()

    # ✅ Create Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sales Report"

    # ✅ Header row
    ws.append(["Dish Name", "Times Ordered", "Total Revenue (₹)"])

    # ✅ Data rows
    for row in rows:
        ws.append(row)

    # ✅ Add total revenue row
    total_revenue = sum(row[2] for row in rows)
    ws.append([])  # empty row for spacing
    ws.append(["", "Total Revenue", total_revenue])

   
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    filename = f"sales_report_{range_type}.xlsx"
    return send_file(
        output,
        download_name=filename,
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
@app.route('/delete_menu_item', methods=['POST'])
def delete_menu_item():
    if session.get('username') != 'admin':
        return redirect('/login')

    item_id = request.form.get('item_id')
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE menu_items SET status = 'deleted' WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    return redirect('/admin')

@app.route('/debug_orders')
def debug_orders():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    print("🔍 Fetching all orders and items...")

    # Fetch all orders
    cursor.execute("SELECT id, user_id, seat_id, total, status, timestamp FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()

    # Fetch all order items
    cursor.execute("""
        SELECT order_items.id, order_items.order_id, menu_items.name
        FROM order_items
        JOIN menu_items ON order_items.item_id = menu_items.id
        ORDER BY order_items.order_id DESC
    """)
    items = cursor.fetchall()

    conn.close()

    return render_template('debug_orders.html', orders=orders, items=items)

if __name__ == '__main__':
	app.run(debug=True)
