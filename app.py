from flask import Flask, render_template
import os

# Point Flask at the subfolder where your templates and static files live
BASE = os.path.join(os.path.dirname(__file__), 'Restaurant-Management-Serve_easy-')

app = Flask(
	__name__,
	static_folder=os.path.join(BASE, 'static'),
	template_folder=os.path.join(BASE, 'templates'),
)


@app.route('/')
def login():
	return render_template('login.html')


if __name__ == '__main__':
	app.run(debug=True)
