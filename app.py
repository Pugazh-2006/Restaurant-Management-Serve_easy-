from flask import Flask, render_template,request,redirect,session
import os
import sqlite3
BASE = os.path.join(os.path.dirname(__file__), 'Restaurant-Management-Serve_easy-')

app = Flask(
	__name__,
	static_folder=os.path.join(BASE, 'static'),
	template_folder=os.path.join(BASE, 'templates'),
)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET','POST'])
def login():
	message = ''
	if request.method == 'POST':
		print("POST method triggered")
		username = request.form['username']
		password = request.form['password']

		conn = sqlite3.connect('restaurant.db')
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
		user = cursor.fetchone()
		conn.close()

		if user:
			session['user_id'] = user[0]
			session['username'] = username
			return redirect('/menu')
		else:
			message = "Invalid username or password"
	return render_template('login.html', message=message)

@app.route('/register' , methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']


		conn = sqlite3.connect('restaurant.db')
		cursor = conn.cursor()

		cursor.execute("SELECT * FROM users WHERE username=?", (username,))
		if cursor.fetchone():
			conn.close()
			return "Username already exists. Try a different one."
		
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
	conn = sqlite3.connect('restaurant.db')
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM menu_items")
	items = []
	for row in cursor.fetchall():
		image = row[3].strip() if row[3] and row[3].strip() else 'masala_dosa.jpg'
		items.append((row[0], row[1], row[2], image))
	conn.close()
	return render_template('menu.html', items=items)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
	item_id = request.form['item_id']
	if 'cart' not in session:
		session['cart'] = []
	session['cart'].append(item_id)
	return redirect('/menu')




if __name__ == '__main__':
	app.run(debug=True)
