from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = {'apiKey': "AIzaSyB7a20VKsYyeXK5vNd9UpccmaUj8xw7cAI",
  'authDomain': "project-2-4fc95.firebaseapp.com",
  'projectId': "project-2-4fc95",
  'storageBucket': "project-2-4fc95.appspot.com",
  'messagingSenderId': "149584278818",
  'appId': "1:149584278818:web:3002322fa5824a790c617b",
  'databaseURL':"https://project-2-4fc95-default-rtdb.europe-west1.firebasedatabase.app/"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Code goes below here
@app.route('/signin', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
	return render_template("signin.html")


@app.route('/', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		full_name = request.form['full_name']
		username = request.form['username']
		age = request.form['age']
		try:
			user = {"email" : email, "password" : password,"full_name" :full_name, "username" : username, "age": age}
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			uid = login_session['user']['localId']
			db.child("Users").child(uid).set(user)
		
			return redirect(url_for('home'))
		except Exception as e:
			print("SIGN UP ERROR:", e)
			error = "Authentication failed"
	return render_template("signup.html")

@app.route('/home', methods = ['GET', 'POST'])
def home():
	#error = ""
	uid = login_session['user']['localId']
	usernamy =db.child("Users").child(uid).get().val()
	return render_template("home.html", usernamy=usernamy["username"])

@app.route('/about', methods = ['GET', 'POST'])
def about():
	#error = ""
	return render_template("about.html")

@app.route('/branches', methods = ['GET', 'POST'])
def branches():
	#error = ""
	return render_template("branches.html")

@app.route('/flavors', methods = ['GET', 'POST'])
def flavors():
	#error = ""
	return render_template("flavors.html")

@app.route('/comments', methods = ['GET', 'POST'])
def comments():
	#error = ""
	return render_template("comments.html")

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)