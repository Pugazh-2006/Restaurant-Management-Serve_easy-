from flask import Flask, render_template,request,redirect 
import os
import sqlite3
BASE = os.path.join(os.path.dirname(__file__), 'Restaurant-Management-Serve_easy-')

app = Flask(
	__name__,
	static_folder=os.path.join(BASE, 'static'),
	template_folder=os.path.join(BASE, 'templates'),
)


@app.route('/', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		print("POST method triggered")
		username = request.form['username']
		password = request.form['password']

		conn = sqlite3.connect('users.db')
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
		user = cursor.fetchone()
		conn.close()

		if user:
			return " Login Successful!"
		else:
			return "Invalid credentials. Try again."
	return render_template('login.html')

@app.route('/register' , methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		conn = sqlite3.connect('users.db')
		cursor = conn.cursor()
		
		cursor.execute("SELECT * FROM users WHERE username=?", (username,))
		if cursor.fetchone():
			conn.close()
			return "Username already exists. Try a different one."
		
		cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
		conn.commit()
		conn.close()
		return render_template('login.html', message="Registration Successful! Please Login.")

	return render_template('register.html')


if __name__ == '__main__':
	app.run(debug=True)
