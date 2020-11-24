from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector
import sys

#Initialize the app from Flask
app = Flask(__name__,
	static_url_path="/",
	static_folder="static")

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
	user='root',
	password='root',
	database='Airtickets',
	port=8889)


#Define a route to hello function
@app.route('/')
def hello():
	if 'email' in session:
		return redirect(url_for('home'))
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM Customer WHERE email = '{}' and password = '{}'"
	cursor.execute(query.format(email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['email'] = email
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
	email = request.form['email']
	username = request.form['username']
	password = request.form['password']
	building_num = request.form['buildingnum']
	if building_num == "": building_num=None
	street = request.form['street']
	if street == "": street=None
	city = request.form['city']
	if city == "": city=None
	state = request.form['state']
	if state == "": state=None
	phone_num = request.form['phonenumber']
	if phone_num == "": phone_num=None
	passport_number = request.form['passportnumber']
	if passport_number == "": passport_number=None
	passport_expiration = request.form['passportexpiration']
	if passport_expiration == "": passport_expiration=None
	passport_country = request.form['passportcountry']
	if passport_country == "": passport_country=None
	date_of_birth = request.form['dob']
	if date_of_birth == "": date_of_birth=None

	print(email, username, password, building_num, street, city, state, phone_num, passport_country, passport_expiration, passport_country, date_of_birth, file=sys.stdout)
    #cursor used to send queries
	cursor = conn.cursor()
    #executes query
	query = "SELECT * FROM Customer WHERE email = '{}'"
	cursor.execute(query.format(email))
    #stores the results in a variable
	data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
	#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = "INSERT INTO Customer VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
		cursor.execute(ins.format(email, username, password, building_num, street, city, state, phone_num, passport_number, passport_expiration, passport_country, date_of_birth))
		conn.commit()
		cursor.close()
		return render_template('index.html')

'''
@app.route('/home')
def home():
    email = session['email']
    cursor = conn.cursor();
    query = "SELECT ts, blog_post FROM blog WHERE username = '{}' ORDER BY ts DESC"
    cursor.execute(query.format(username))
    data1 = cursor.fetchall() 
    cursor.close()
    return render_template('home.html', email=username, posts=data1)
	
@app.route('/post', methods=['GET', 'POST'])
def post():
	email = session['email']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = "INSERT INTO blog (blog_post, email) VALUES('{}', '{}')"
	cursor.execute(query.format(blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))
'''

@app.route('/logout')
def logout():
	session.pop('email')
	return redirect('/')
	
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 8888, debug = True)
