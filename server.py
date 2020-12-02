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

	if login_type == 'airline_staff':
		username = request.form['username']
		password = request.form['password']

		cursor = conn.cursor()
		query = "SELECT * FROM {} WHERE username = '{}' and password = '{}'"
		cursor.execute(query.format(login_type, username, password))

		data = cursor.fetchone()
		cursor.close()
		error = None
		if(data):
			session['username'] = username
			return redirect(url_for('sViewFlight'))
		else:
			error = 'Invalid login or username'
			return render_template('login.html', error=error)
	elif login_type == "customer":
		email = request.form['email']
		password = request.form['password']

		#cursor used to send queries
		cursor = conn.cursor()
		#executes query
		query = "SELECT * FROM {} WHERE email = '{}' and password = '{}'"
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
			return redirect(url_for('cViewFlight'))
		else:
			#returns an error message to the html page
			error = 'Invalid login or username'
			return render_template('login.html', error=error)
	else:
		email = request.form['email']
		password = request.form['password']

		#cursor used to send queries
		cursor = conn.cursor()
		#executes query
		query = "SELECT * FROM {} WHERE email = '{}' and password = '{}'"
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
			return redirect(url_for('baViewFlight'))
		else:
			#returns an error message to the html page
			error = 'Invalid login or username'
			return render_template('login.html', error=error)


#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
	login_type = request.form['login-type']

	if login_type == 'customer':
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		building_num = request.form['buildingnum']
		street = request.form['street']
		city = request.form['city']
		state = request.form['state']
		phone_num = request.form['phonenumber']
		passport_number = request.form['passportnumber']
		passport_expiration = request.form['passportexpiration']
		passport_country = request.form['passportcountry']
		date_of_birth = request.form['dob']
		print(email, username, password, building_num, street, city, state, phone_num, passport_country, passport_expiration, passport_country, date_of_birth, file=sys.stdout)
		#cursor used to send queries
		cursor = conn.cursor()
		#executes query
		query = "SELECT * FROM customer WHERE email = '{}'"
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
			ins = "INSERT INTO customer VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
			cursor.execute(ins.format(email, username, password, building_num, street, city, state, phone_num, passport_number, passport_expiration, passport_country, date_of_birth))
			conn.commit()
			cursor.close()
			return render_template('index.html')
	elif login_type == 'airline_staff':
		username = request.form['username-as']
		password = request.form['password-as']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		date_of_birth = request.form['dob-as']
		airline_name = request.form['airline_name']

		cursor = conn.cursor()
		query = "SELECT * FROM airline_staff WHERE username = '{}'"
		cursor.execute(query.format(username))
		data = cursor.fetchone()
		error = None
		if(data):
			return render_template('register.html', error = error)
		else:
			ins = "INSERT INTO airline_staff VALUES('{}', '{}', '{}', '{}', '{}', '{}')"
			cursor.execute(ins.format(username, password, first_name, last_name, date_of_birth, airline_name))
			conn.commit()
			cursor.close()
			return render_template('index.html')
	elif login_type == 'booking_agent':
		email = request.form['email-ba']
		password = request.form['password-ba']
		cursor = conn.cursor()
		query = "SELECT * FROM booking_agent WHERE email = '{}'"
		cursor.execute(query.format(email))
		data = cursor.fetchone()
		error = None
		if(data):
			return render_template('register.html', error = error)
		else:
			query = "SELECT booking_agent_id FROM booking_agent"
			cursor.execute(query)
			BA_ids = cursor.fetchall()
			booking_agent_id = str(int(BA_ids[-1][0]) + 1)
			
			ins = "INSERT INTO booking_agent VALUES('{}', '{}', '{}')"
			cursor.execute(ins.format(email, password, booking_agent_id))
			conn.commit()
			cursor.close()
			return render_template('index.html')


@app.route('/home')
def home():
    email = session['email']
    cursor = conn.cursor()
    query = "SELECT * FROM purchases WHERE customer_email = '{}' ORDER BY customer_email DESC"
    cursor.execute(query.format(email))
    data1 = cursor.fetchall() 
    cursor.close()
    return render_template('home.html', email=email, posts=data1)

#Match input of city/airport to the corresponding airport
@app.route('/airport')
def airport(name):
	cursor = conn.cursor()
	query = "SELECT airport_name FROM airport WHERE airport_name = '{}'"
	cursor.execute(query.format(name))
	data = cursor.fetchone()
	if data: # if the input is a airport name
		cursor.close()
		return(name)
	else:
		query = "SELECT airport_name FROM airport WHERE airport_city = '{}'"
		cursor.execute(query.format(name))
		data = cursor.fetchone()
		cursor.close()
		error = None
		if data: # if the input is a city name
			return(data[0])
		else: # if the input is invalid
			return error

#Search for upcoming flights
@app.route('/search', methods=['GET', 'POST'])
def search():
	source = airport(request.form['source'])
	destination = airport(request.form['destination'])
	date = request.form['date']
	cursor = conn.cursor()
	query = """SELECT * FROM flight WHERE departure_airport = "{}" and arrival_airport = '{}' and DATE(departure_time) = '{}'"""
	cursor.execute(query.format(source, destination, date))
	data = cursor.fetchall()
	if request.form['flight-type'] == "roundtrip": # roundtrip
		back_date = request.form['back-date']
		cursor.execute(query.format(destination, source, back_date))
		data.extend(cursor.fetchall())
	cursor.close()
	return render_template('result.html', email=email, data=data)

#--------------------------Customer Use Case--------------------------
@app.route('/cViewFlight')
def cViewFlight():
	email = session['email']
	cursor = conn.cursor()
	query = """SELECT * FROM flight WHERE flight_num IN (SELECT flight_num FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE customer_email='{}') ORDER BY departure_time""" # AND departure_time > NOW()
	cursor.execute(query.format(email))
	data = cursor.fetchall()
	cursor.close()
	return render_template('c_viewflight.html', email=email, data=data)

#Customer searches for upcoming flights and purchases tickets
@app.route('/cPurchase')
def cPurchase():
	return

@app.route('/cSpending')
def cSpending():
	email = session['email']
	cursor = conn.cursor()
	query = """SELECT SUM(price) FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE customer_email='{}' AND 
			purchase_date BETWEEN date_sub(NOW(), INTERVAL 1 year) and NOW()"""
	cursor.execute(query.format(email))
	last_year = cursor.fetchall()

	query = """SELECT SUM(price) FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE customer_email='{}' AND 
			purchase_date BETWEEN date_sub(NOW(), INTERVAL '{}' month) and date_sub(NOW(), INTERVAL '{}' month)"""
			# or '{}' month ???
	bar_data = []
	for i in range(0,6):
		cursor.execute(query.format(email, str(i+1), str(i)))
		bar_data.append(cursor.fetchall()[0])

	# option: range of dates

	cursor.close()
	error = None
	return render_template('c_spending.html', email=email, last_year=last_year, bar_data=bar_data, error=error)

#------------------------Booking Agent Use Case------------------------
@app.route('/baViewFlight')
def baViewFlight():
	email = session['email']
	cursor = conn.cursor()
	query = """SELECT * FROM flight WHERE flight_num IN (SELECT flight_num FROM flight NATURAL JOIN ticket NATURAL JOIN purchases 
			NATURAL JOIN booking_agent WHERE email='{}') ORDER BY departure_time""" # AND departure_time > NOW()
	cursor.execute(query.format(email))
	data = cursor.fetchall()
	cursor.close()
	return render_template('ba_viewflight.html', email=email, data=data)

#Booking agent searches for upcoming flights and purchases tickets for other customers
@app.route('/baPurchase')
def baPurchase():
	return

@app.route('/baComission')
def baComission():
	email = session['email']
	cursor = conn.cursor()
	query = """SELECT SUM(price), COUNT(ticket_id) FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight 
			WHERE purchase_date BETWEEN date_sub(NOW(), INTERVAL 30 day) and NOW() GROUP BY email HAVING email = '{}'"""
	cursor.execute(query.format(email))
	total_com, num_tickets = cursor.fetchone()
	cursor.close()
	data = tuple([total_com, total_com/num_tickets, num_tickets])
	return render_template('ba_comission.html', email=email, data=data)

@app.route('/baCustomer')
def baCustomer():
	email = session['email']
	cursor = conn.cursor()
	query = """SELECT customer_email FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE purchase_date 
			BETWEEN date_sub(NOW(), INTERVAL 6 month) and NOW() GROUP BY email ORDER BY SUM(price) DESC HAVING email = '{}' LIMIT 5"""
	cursor.execute(query.format(email))
	data = cursor.fetchall()
	cursor.close()
	return render_template('ba_customer.html', email=email, data=data)

#------------------------Ailine Staff Use Case------------------------
@app.route('/sViewFlight')
def sViewFlight():
	username = session['username']
	cursor = conn.cursor()
	query = "SELECT airline_name FROM airline_staff WHERE username = '{}'"
	cursor.execute(query.format(username))
	airline_name = cursor.fetchone()[0]

	query = "SELECT * FROM flight WHERE airline_name = '{}' ORDER BY airline_name DESC"
	cursor.execute(query.format(airline_name))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('as_viewflight.html', username=username, datas=data1)

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
	username = session['username']
	cursor = conn.cursor()
	query = """SELECT email FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff WHERE purchase_date 
			BETWEEN date_sub(NOW(), INTERVAL '{}') and NOW() AND username = '{}' GROUP BY email ORDER BY COUNT(ticket_id) DESC LIMIT 5"""
	cursor.execute(query.format('1 month', username))
	data = cursor.fetchall()
	cursor.execute(query.format('1 year', username))
	data.extend(cursor.fetchall())

	query = """SELECT email FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff WHERE purchase_date 
			BETWEEN date_sub(NOW(), INTERVAL 1 year) and NOW() AND username = '{}' GROUP BY email ORDER BY SUM(price) DESC LIMIT 5"""
	cursor.execute(query.format(username))
	data.extend(cursor.fetchall())
	cursor.close()
	error = None
	return render_template('as_viewBA.html', username=username, data=data, error=error)

@app.route('/sViewCustomer')
def sViewCustomer():
	customer = request.form['customer'] # input
	username = session['username']

	cursor = conn.cursor()
	query = """SELECT customer_email FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE purchase_date 
			BETWEEN date_sub(NOW(), INTERVAL 1 year) and NOW() GROUP BY customer_email ORDER BY COUNT(ticket_id) DESC"""
	cursor.execute(query)
	customers = cursor.fetchall()

	query = """SELECT DISTINCT flight_num FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff 
			WHERE customer_email = '{}' AND username = '{}'"""
	cursor.execute(query.format(customer, username))
	flights = cursor.fetchall() # a list of all flights a particular Customer has taken only on that particular airline.
	cursor.close()
	error = None

	return render_template('as_viewCustomer.html', username=username, customers=customers, flights=flights, error=error)

@app.route('/sViewReport')
def sViewReport():
	username = session['username']

	# To do: range of dates

	cursor = conn.cursor()
	query = """SELECT SUM(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff WHERE username = '{}'
			AND purchase_date BETWEEN date_sub(NOW(), INTERVAL 1 year) and NOW()"""
	cursor.execute(query.format(username, 'year'))
	last_year = cursor.fetchone()[0]

	query = """SELECT SUM(price) FROM flight NATURAL JOIN ticket NATURAL JOIN purchases NATURAL JOIN airline_staff WHERE username = '{}' 
			AND purchase_date BETWEEN date_sub(NOW(), INTERVAL {} month) and date_sub(NOW(), INTERVAL {} month)"""
	bar_data = []
	for i in range(0,6):
		cursor.execute(query.format(email), str(i+1), str(i))
		bar_data.append(cursor.fetchone()[0])
	cursor.close()
	error = None
	return render_template('as_viewReport.html', username=username, last_year=last_year, bar_data=bar_data, error=error)

@app.route('/sViewDestination')
def sViewDestination():
	username = session['username']
	cursor = conn.cursor()
	query = """SELECT arrival_airport FROM ticket NATURAL JOIN flight NATURAL JOIN purchases NATURAL JOIN airline_staff 
			WHERE username = '{}' AND purchase_date BETWEEN date_sub(NOW(), INTERVAL {}) and NOW() GROUP BY arrival_airport 
			ORDER BY COUNT(ticket_id) DESC LIMIT 3"""
	cursor.execute(query.format(username, '3 month'))
	last_3months = cursor.fetchall()
	cursor.execute(query.format(username, '1 year'))
	last_year = cursor.fetchall()
	cursor.close()
	error = None
	return render_template('as_viewDestination.html', username=username, last_year=last_year, last_3months=last_3months, error=error)

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
	try:
		session.pop('email')
		return redirect('/')
	except:
		session.pop('username')
		return redirect('/')
	
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
