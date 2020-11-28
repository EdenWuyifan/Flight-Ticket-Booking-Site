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
	login_type = request.form['login-type']

	if login_type == 'AirlineStaff':
		username = request.form['username']
		password = request.form['password']

		cursor = conn.cursor()
		query = "SELECT * FROM {} WHERE username = '{}' and pwd = '{}'"
		cursor.execute(query.format(login_type, username, password))

		data = cursor.fetchone()
		cursor.close()
		error = None
		if(data):
			session['username'] = username
			return redirect(url_for('home'))
		else:
			error = 'Invalid login or username'
			return render_template('login.html', error=error)
	else:
		email = request.form['email']
		password = request.form['password']

		#cursor used to send queries
		cursor = conn.cursor()
		#executes query
		query = "SELECT * FROM {} WHERE email = '{}' and pwd = '{}'"
		cursor.execute(query.format(login_type, email, password))
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
	login_type = request.form['login-type']

	if login_type == 'Customer':
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
	elif login_type == 'AirlineStaff':
		username = request.form['username']
		password = request.form['password']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		date_of_birth = request.form['dob']
		airline_name = request.form['airline_name']

		cursor = conn.cursor()
		query = "SELECT * FROM AirlineStaff WHERE username = '{}'"
		cursor.execute(query.format(username))
		data = cursor.fetchone()
		error = None
		if(data):
			return render_template('register.html', error = error)
		else:
			ins = "INSERT INTO AirlineStaff VALUES('{}', '{}', '{}', '{}', '{}', '{}')"
			cursor.execute(ins.format(username, password, first_name, last_name, date_of_birth, airline_name))
			conn.commit()
			cursor.close()
			return render_template('index.html')
	else:
		email = request.form['email']
		password = request.form['password']
		
		print(email, password, file=sys.stdout)
		cursor = conn.cursor()
		query = "SELECT * FROM BookingAgent WHERE email = '{}'"
		cursor.execute(query.format(email))
		data = cursor.fetchone()
		error = None
		if(data):
			return render_template('register.html', error = error)
		else:
			query = "SELECT booking_agent_id FROM BookingAgent"
			cursor.execute(query)
			BA_ids = cursor.fetchall()
			booking_agent_id = str(int(BA_ids[-1][0]) + 1)
			
			email = request.form['email']
			password = request.form['password']
			ins = "INSERT INTO BookingAgent VALUES('{}', '{}', '{}')"
			cursor.execute(ins.format(email, password, booking_agent_id))
			conn.commit()
			cursor.close()
			return render_template('index.html')


@app.route('/home')
def home():
    email = session['email']
    cursor = conn.cursor()
    query = "SELECT * FROM purchases WHERE C_email = '{}' ORDER BY C_email DESC"
    cursor.execute(query.format(email))
    data1 = cursor.fetchall() 
    cursor.close()
    return render_template('home.html', email=email, posts=data1)

#Search for upcoming flights
@app.route('/search')
def search():
	flight_type = request.form["flight-type"]
	source = request.form['source']
	#source_airport = request.form['source-airport']
	destination = request.form['destination']
	#destination_airport = request.form['destination-airport']
	date = request.form['date']
	if flight_type == "roundtrip":
		cursor = conn.cursor()
		query = "SELECT * FROM flight WHERE departure_airport = '{}' and arrival_ariport = '{}' and DATE(departure_time) = {}"
		cursor.execute(query.format(source, destination, date))

		data = cursor.fetchone()
		cursor.close()
		error = None

	return

#--------------------------Customer Use Case--------------------------
@app.route('/cViewFlight')
def cViewFlight():
	return

#Customer searches for upcoming flights and purchases tickets
@app.route('/cPurchase')
def cPurchase():
	search()
	return

@app.route('/cSpending')
def cSpending():
	return

#------------------------Booking Agent Use Case------------------------
@app.route('/baViewFlight')
def baViewFlight():
	return

#Booking agent searches for upcoming flights and purchases tickets for other customers
@app.route('/baPurchase')
def baPurchase():
	return

@app.route('/baComission')
def baComission():
	return

@app.route('/baCustomer')
def baCustomer():
	return

#------------------------Ailine Staff Use Case------------------------
@app.route('/sViewFlight')
def sViewFlight():
	return

@app.route('/createFlight')
def createFlight():
	return

@app.route('/changeStatus')
def changeStatus():
	return

@app.route('/addAirplane')
def addAirplane():
	return

@app.route('/addAirport')
def addAirport():
	return

@app.route('/sViewBA')
def sViewBA():
	return

@app.route('/sViewCustomer')
def sViewCustomer():
	return

@app.route('/sViewReport')
def sViewReport():
	return

@app.route('/sViewDestination')
def sViewDestination():
	return

'''
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
	app.run('127.0.0.1', 5000, debug = True)
