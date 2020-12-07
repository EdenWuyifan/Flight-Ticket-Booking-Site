from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector
import sys
import math

#Initialize the app from Flask
app = Flask(__name__,
	static_url_path="/",
	static_folder="static")

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
	user='root',
	password='root',
	database='Airtickets',
	port=8889,
	buffered=True
	)


#Define a route to hello function
@app.route('/')
def hello():
	#To be change
	if 'email' in session:
		return redirect(url_for('cViewFlight'))
	elif 'email_b' in session:
		return redirect(url_for('baViewFlight'))
	elif 'username' in session:
		return redirect(url_for('sViewFlight'))
	cursor = conn.cursor()
	query_1 = "SELECT * FROM airport"
	cursor.execute(query_1)
	airports = cursor.fetchall()
	cursor.close()
	return render_template('index.html', airports=airports)

#Define route for login
@app.route('/login')
def login():
	error = None
	return render_template('login.html', error=error)

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
			session['email_b'] = email
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
		#print(email, username, password, building_num, street, city, state, phone_num, passport_country, passport_expiration, passport_country, date_of_birth, file=sys.stdout)
		error = None
		if len(email) == 0:
			error = "Please enter your email!"
			return render_template('register.html', error = error)
		#cursor used to send queries
		cursor = conn.cursor()
		#executes query
		query = "SELECT * FROM customer WHERE email = '{}'"
		cursor.execute(query.format(email))
		#stores the results in a variable
		data = cursor.fetchone()
		#use fetchall() if you are expecting more than 1 data row
		if(data):
		#If the previous query returns data, then user exists
			error = "This user already exists"
			return render_template('register.html', error = error)
		if username=='' or password=='' or building_num=='' or street=='' or city=='' or state=='' or phone_num=='' or passport_number=='' or passport_expiration=='' or passport_country=='' or date_of_birth=='':
			error = "Please fill out all your information!"
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
		error = None
		if len(username) == 0:
			error = "Please enter your username!"
			return render_template('register.html', error = error)
		cursor = conn.cursor()
		query = "SELECT * FROM airline_staff WHERE username = '{}'"
		cursor.execute(query.format(username))
		data = cursor.fetchone()
		if(data):
			error = "This user already exists"
			return render_template('register.html', error = error)
		if password=='' or first_name=='' or last_name=='' or date_of_birth=='' or airline_name=='':
			error = "Please fill out all your information!"
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
		error = None
		cursor = conn.cursor()
		query = "SELECT * FROM booking_agent WHERE email = '{}'"
		cursor.execute(query.format(email))
		data = cursor.fetchone()
		if(data):
			error = "This user already exists"
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

#Match input of city/airport to the corresponding airport
'''
@app.route('/airport')
def airport(name):
	cursor = conn.cursor()
	query = """SELECT airport_name FROM airport WHERE airport_name = "{}" """
	cursor.execute(query.format(name))
	data = cursor.fetchone()
	if data: # if the input is a airport name
		cursor.close()
		return(name)
	else:
		query = """SELECT airport_name FROM airport WHERE airport_city = "{}" """
		cursor.execute(query.format(name))
		data = cursor.fetchone()
		cursor.close()
		error = None
		if data: # if the input is a city name
			return(data[0])
		else: # if the input is invalid
			return error
'''
#Search for upcoming flights
@app.route('/search', methods=["POST"])
def search():

	source = request.form['source']
	destination = request.form['destination']
	date = request.form['date']
	cursor = conn.cursor()
	if len(date) != 0:
		query = """SELECT * FROM flight WHERE departure_airport = "{}" and arrival_airport = "{}" and DATE(departure_time) = '{}' """
		cursor.execute(query.format(source, destination, date))
	else: # user didn't enter a date
		query = """SELECT * FROM flight WHERE departure_airport = "{}" and arrival_airport = "{}" """
		cursor.execute(query.format(source, destination))
	data = cursor.fetchall()
	cursor.close()
	return render_template('result.html', data=data)

#--------------------------Customer Use Case--------------------------
@app.route('/cViewFlight')
def cViewFlight():
	email = session['email']
	cursor = conn.cursor()
	query = """SELECT * FROM flight WHERE flight_num IN (SELECT flight_num FROM flight NATURAL JOIN ticket NATURAL JOIN purchases 
			WHERE customer_email='{}' AND departure_time > NOW()) ORDER BY departure_time"""
	cursor.execute(query.format(email))
	data = cursor.fetchall()
	cursor.close()
	return render_template('c_viewflight.html', email=email, data=data)
	
# Optionally you may include a way for the user to specify a range of dates, specify destination and/or source airport name or city name etc.
@app.route('/cViewFlight', methods=['POST'])
def cViewFlightSearch():
	email = session['email']
	start = request.form['start']
	end = request.form['end']
	cursor = conn.cursor()
	# Allow to specify a range of dates
	query = "SELECT * FROM flight WHERE flight_num IN (SELECT flight_num FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE customer_email='{}' AND departure_time BETWEEN '{} 00:00:00' AND '{} 00:00:00') ORDER BY departure_time"
	cursor.execute(query.format(email, start, end))
	print(query.format(email, start, end))
	data = cursor.fetchall()
	cursor.close()
	return render_template('c_viewflight.html', email=email, data=data)	

#Customer searches for upcoming flights and purchases tickets
@app.route('/cPurchaseSearch')
def cLoadSearch():
	email =  session['email']
	error = None

	cursor = conn.cursor()
	query_1 = "SELECT * FROM airport"
	cursor.execute(query_1)
	airports = cursor.fetchall()
	cursor.close()
	return render_template('c_search.html', email=email, error=error, airports=airports)

@app.route('/cPurchaseSearch', methods=["POST"])
def cLoadPurchaseInfo():
	email = session['email']
	source = request.form['source'] # inputs
	destination = request.form['destination']
	date = request.form['date'] #
	error = None
	cursor = conn.cursor()
	if len(date) != 0:
		query = """SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id
				FROM flight NATURAL JOIN ticket NATURAL JOIN airplane WHERE departure_airport = "{}" and arrival_airport = "{}" AND 
				DATE(departure_time) = '{}' GROUP BY airline_name, flight_num, seats HAVING seats > COUNT(ticket_id)"""
		cursor.execute(query.format(source, destination, date))
	else:
		query = """SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id
				FROM flight NATURAL JOIN ticket NATURAL JOIN airplane WHERE departure_airport = "{}" and arrival_airport = "{}" 
				GROUP BY airline_name, flight_num, seats HAVING seats > COUNT(ticket_id)"""
		cursor.execute(query.format(source, destination))
	data = cursor.fetchall()
	if source == destination:
		error="Source and Destination connot be the same!"
		query_1 = "SELECT * FROM airport"
		cursor.execute(query_1)
		airports = cursor.fetchall()
		cursor.close()
		return render_template('c_search.html', email=email, error=error, airports=airports)
	else:
		cursor.close()
		return render_template('c_purchase.html', email=email, error=error, data=data)

@app.route('/cPurchase', methods=["POST"])
def cPurchase():
	email = session['email']
	data_index = int(request.form["data-index"])-1	
	flight_num  = request.form.getlist("flight_num")[data_index] # inputs
	airline_name = request.form.getlist('airline_name')[data_index] #
	error = None

	cursor = conn.cursor()
	"""
	query_1 = "SELECT * FROM airport"
	cursor.execute(query_1)
	airports = cursor.fetchall()
	"""

	query_2 = "SELECT * FROM flight WHERE flight_num={}"
	cursor.execute(query_2.format(flight_num))
	flight = (cursor.fetchone(),)

	query = "SELECT ticket_id FROM purchases"
	cursor.execute(query)
	t_ids = cursor.fetchall()
	t_ids.sort()
	if len(t_ids) == 0:
		ticket_id = 1
	else:
		ticket_id = str(int(t_ids[-1][0]) + 1)

	query = """INSERT INTO ticket VALUES ('{}','{}','{}');"""
	cursor.execute(query.format(ticket_id, airline_name, flight_num))

	query = """INSERT INTO purchases VALUES ('{}','{}', NULL, DATE(NOW()));"""
	cursor.execute(query.format(ticket_id, email))
	query = """SELECT flight_num FROM flight WHERE flight_num IN (SELECT flight_num FROM flight NATURAL JOIN ticket NATURAL JOIN purchases 
			WHERE customer_email='{}' AND departure_time > NOW()) ORDER BY departure_time"""
	cursor.execute(query.format(email))
	purchases_have_been_made = cursor.fetchall()

	if (int(flight_num),) in purchases_have_been_made:
		error = "You have already booked this flight!"
		query_1 = "SELECT * FROM airport"
		cursor.execute(query_1)
		airports = cursor.fetchall()
		cursor.close()
		return render_template('c_search.html', email=email, error=error, airports=airports)
	else:
		conn.commit()
		cursor.close()
		return render_template('purchase_success.html', email=email, error=error, flight=flight)

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
	bar_data = ()
	for i in range(0,6):
		cursor.execute(query.format(email, str(i+1), str(i)))
		spend = cursor.fetchone()
		if spend[0] == None:
			spend = (0,)
		bar_data += spend
	bar_data = (bar_data, )

	# option: range of dates

	cursor.close()
	error = None
	return render_template('c_spending.html', email=email, last_year=last_year, bar_data=bar_data, error=error)

#------------------------Booking Agent Use Case------------------------
@app.route('/baViewFlight')
def baViewFlight():
	email = session['email_b']
	cursor = conn.cursor()
	query = """SELECT * FROM flight WHERE flight_num IN (SELECT flight_num FROM flight NATURAL JOIN ticket NATURAL JOIN purchases 
			NATURAL JOIN booking_agent WHERE email='{}') ORDER BY departure_time""" # AND departure_time > NOW()
	cursor.execute(query.format(email))
	data = cursor.fetchall()
	cursor.close()
	return render_template('ba_viewflight.html', email_b=email, data=data)

@app.route('/baViewFlight', methods=['POST'])
def baViewFlightSearch():
	email = session['email_b']
	start = request.form['start']
	end = request.form['end']
	cursor = conn.cursor()
	# Allow to specify a range of dates
	query = """SELECT * FROM flight WHERE flight_num IN (SELECT flight_num FROM flight NATURAL JOIN ticket NATURAL JOIN purchases NATURAL JOIN booking_agent
	 			WHERE email='{}' AND departure_time BETWEEN '{} 00:00:00' AND '{} 00:00:00') ORDER BY departure_time"""
	cursor.execute(query.format(email, start, end))
	print(query.format(email, start, end))
	data = cursor.fetchall()
	cursor.close()
	return render_template('ba_viewflight.html', email_b=email, data=data)	

#Booking agent searches for upcoming flights and purchases tickets for other customers
@app.route('/baPurchaseSearch')
def baLoadSearch():
	email =  session['email_b']
	error = None

	cursor = conn.cursor()
	query_1 = "SELECT * FROM airport"
	cursor.execute(query_1)
	airports = cursor.fetchall()
	cursor.close()
	return render_template('ba_search.html', email_b=email, error=error, airports=airports)

@app.route('/baPurchaseSearch', methods=["POST"])
def baLoadPurchaseInfo():
	email = session['email_b']
	source = request.form['source'] # inputs
	destination = request.form['destination']
	date = request.form['date'] #
	error = None
	
	cursor = conn.cursor()
	query_1 = "SELECT * FROM customer"
	cursor.execute(query_1)
	customers = cursor.fetchall()

	if len(date) != 0:
		query = """SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id
				FROM flight NATURAL JOIN ticket NATURAL JOIN airplane WHERE departure_airport = "{}" and arrival_airport = "{}" AND 
				DATE(departure_time) = '{}' GROUP BY airline_name, flight_num, seats HAVING seats > COUNT(ticket_id)"""
		cursor.execute(query.format(source, destination, date))
	else:
		query = """SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id
				FROM flight NATURAL JOIN ticket NATURAL JOIN airplane WHERE departure_airport = "{}" and arrival_airport = "{}" 
				GROUP BY airline_name, flight_num, seats HAVING seats > COUNT(ticket_id)"""
		cursor.execute(query.format(source, destination))
	data = cursor.fetchall()
	
	if source == destination:
		error = "Source and Destination cannot be the same!"
		query_1 = "SELECT * FROM airport"
		cursor.execute(query_1)
		airports = cursor.fetchall()
		cursor.close()
		return render_template('ba_search.html', email_b=email, error=error, airports=airports)
	else:
		cursor.close()
		return render_template('ba_purchase.html', email_b=email, error=error, data=data, customers=customers)

@app.route('/baPurchase', methods=["POST"])
def baPurchase():
	email = session['email_b']
	data_index = int(request.form["data-index"])-1
	flight_num  = request.form.getlist("flight_num")[data_index] # inputs
	airline_name = request.form.getlist('airline_name')[data_index] #
	customer_email = request.form['customer_email']
	error = None

	cursor = conn.cursor()

	query_1 = "SELECT booking_agent_id FROM booking_agent WHERE email='{}'"
	cursor.execute(query_1.format(email))
	booking_agent_id = cursor.fetchone()

	query_2 = "SELECT * FROM flight WHERE flight_num={}"
	cursor.execute(query_2.format(flight_num))
	flight = (cursor.fetchone(),)

	query = "SELECT ticket_id FROM purchases"
	cursor.execute(query)
	t_ids = cursor.fetchall()
	t_ids.sort()
	if len(t_ids) == 0:
		ticket_id = 1
	else:
		ticket_id = str(int(t_ids[-1][0]) + 1)

	query = """INSERT INTO ticket VALUES ('{}','{}','{}');"""
	cursor.execute(query.format(ticket_id, airline_name, flight_num))
	print(ticket_id, airline_name, flight_num)
	query = """INSERT INTO purchases VALUES ('{}','{}', {}, DATE(NOW()));"""
	cursor.execute(query.format(ticket_id, customer_email, int(booking_agent_id[0])))
	query = """SELECT flight_num FROM flight WHERE flight_num IN (SELECT flight_num FROM flight NATURAL JOIN ticket NATURAL JOIN purchases 
			NATURAL JOIN booking_agent WHERE email='{}' and customer_email='{}') ORDER BY departure_time"""
	cursor.execute(query.format(email, customer_email))
	purchases_have_been_made = cursor.fetchall()

	if (int(flight_num),) in purchases_have_been_made:
		error = "Your customer have already booked this flight!"
		query_1 = "SELECT * FROM airport"
		cursor.execute(query_1)
		airports = cursor.fetchall()
		cursor.close()
		return render_template('ba_search.html', email_b=email, error=error, airports=airports)
	else:
		conn.commit()
		cursor.close()
		return render_template('purchase_success.html', email_b=email, error=error, flight=flight)


@app.route('/baComission')
def baComission():
	email = session['email_b']
	cursor = conn.cursor()
	query = """SELECT SUM(price), COUNT(ticket_id) FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight 
			WHERE purchase_date BETWEEN date_sub(NOW(), INTERVAL 30 day) and NOW() GROUP BY email HAVING email = '{}'"""
	cursor.execute(query.format(email))
	try:
		total_com, num_tickets = cursor.fetchone()
		data = ([total_com, total_com/num_tickets, num_tickets],)
	except:
		data = ([0, 0, 0],)
	cursor.close()
	print(data)
	return render_template('ba_comission.html', email_b=email, data=data)
@app.route('/baComission',methods=["POST"])
def baComissionSearch():
	email = session['email_b']
	start = request.form['start']
	end = request.form['end']
	cursor = conn.cursor()
	query = """SELECT SUM(price), COUNT(ticket_id) FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight 
			WHERE purchase_date BETWEEN '{} 00:00:00' AND '{} 00:00:00' GROUP BY email HAVING email = '{}'"""
	cursor.execute(query.format(start,end,email))
	try:
		total_com, num_tickets = cursor.fetchone()
		data = ([total_com, math.floor(total_com/num_tickets), num_tickets],)
	except:
		data = ([0,0,0],)
	cursor.close()
	
	return render_template('ba_comission.html', email_b=email, data=data)

@app.route('/baCustomer')
def baCustomer():
	email = session['email_b']
	cursor = conn.cursor()
	query = """SELECT customer_email, SUM(price) FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE purchase_date 
   				BETWEEN date_sub(NOW(), INTERVAL 6 month) and NOW() and email = '{}' GROUP BY customer_email ORDER BY SUM(price) DESC LIMIT 5"""
	cursor.execute(query.format(email))
	data1 = cursor.fetchall()
	query = """SELECT customer_email, COUNT(ticket_id) FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE email = '{}' AND 
				purchase_date BETWEEN date_sub(NOW(), INTERVAL 1 year) and NOW() GROUP BY customer_email ORDER BY COUNT(ticket_id) DESC LIMIT 5"""
	cursor.execute(query.format(email))
	data2 = cursor.fetchall()
	cursor.close()
	return render_template('ba_customer.html', email_b=email, data1=data1, data2=data2)

#------------------------Ailine Staff Use Case------------------------
@app.route('/sViewFlight')
def sViewFlight():
	username = session['username']
	cursor = conn.cursor()
	query = "SELECT airline_name FROM airline_staff WHERE username = '{}'"
	cursor.execute(query.format(username))
	airline_name = cursor.fetchone()[0]

	# Defaults will be showing all the upcoming flights operated by the airline he/she works for the next 30 days.
	query = """SELECT * FROM flight WHERE airline_name = '{}' AND departure_time BETWEEN NOW() AND date_add(NOW(), INTERVAL 30 day) ORDER BY departure_time"""
	cursor.execute(query.format(airline_name))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('as_viewflight.html', username=username, datas=data1)

@app.route('/sViewFlight',methods=['POST'])
def sViewFlightSearch():
	username = session['username']
	start = request.form['start']
	end = request.form['end']
	cursor = conn.cursor()
	query = "SELECT airline_name FROM airline_staff WHERE username = '{}'"
	cursor.execute(query.format(username))
	airline_name = cursor.fetchone()[0]

	# Allow to specify a range of dates
	query = """SELECT * FROM flight WHERE airline_name = '{}' AND departure_time BETWEEN {} AND {} ORDER BY departure_time"""
	cursor.execute(query.format(airline_name, start, end))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('as_viewflight.html', username=username, datas=data1)

@app.route('/createFlight')
def loadPage():
	username = session['username']
	cursor = conn.cursor()
	query = "SELECT DISTINCT {} FROM airplane"
	cursor.execute(query.format("airline_name"))
	airlines = cursor.fetchall()
	
	query_1 = "SELECT DISTINCT airport_name FROM airport"
	cursor.execute(query_1)
	airports = cursor.fetchall()

	query_2 = "SELECT DISTINCT airline_name,airplane_id FROM airplane"
	cursor.execute(query_2)
	airplanes = cursor.fetchall()

	cursor.close()

	error = None
	return render_template('as_createFlight.html', username=username, error=error, airlines=airlines, airports=airports, airplanes=airplanes)

@app.route('/createFlight',methods=['POST'])
def createFlight():

	cursor = conn.cursor()
	query = "SELECT DISTINCT {} FROM airplane"
	cursor.execute(query.format("airline_name"))
	airlines = cursor.fetchall()
	
	query_1 = "SELECT DISTINCT airport_name FROM airport"
	cursor.execute(query_1)
	airports = cursor.fetchall()

	query_2 = "SELECT DISTINCT airline_name,airplane_id FROM airplane"
	cursor.execute(query_2)
	airplanes = cursor.fetchall()

	username = session['username']
	airline_name = request.form['airline'] # inputs
	flight_num = request.form['flightNumber']
	departure_airport = request.form['departureAirport']
	departure_time = request.form['departureTime']
	arrival_airport = request.form['arrivalAirport']
	arrival_time = request.form['arrivalTime']
	price = request.form['price']
	status = request.form['status']
	airplane_id = request.form['airplaneId'] #
	error = None

	cursor = conn.cursor()
	query = """ SELECT * FROM flight WHERE airline_name = "{}" AND flight_num = "{}" """
	cursor.execute(query.format(airline_name, flight_num))
	result = cursor.fetchone()
	if result:
		error = "This flight already exists"
		return render_template('as_createFlight.html', username=username, error=error, airlines=airlines, airports=airports, airplanes=airplanes)
	else:
		query = """INSERT INTO `flight` VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}");"""
		cursor.execute(query.format(airline_name,flight_num,departure_airport,departure_time,arrival_airport,arrival_time,price,status,airplane_id))
		#print(query.format(airline_name,flight_num,departure_airport,departure_time,arrival_airport,arrival_time,price,status,airplane_id), file=sys.stdout)
		conn.commit()
		cursor.close()
		#return render_template('as_createFlight.html', username=username, error=error, airlines=airlines, airports=airports, airplanes=airplanes)
		return render_template('as_success.html', username=username, error=error)


@app.route('/changeStatus')
def changeStatusLoad():
	username = session['username']
	error = None
	cursor = conn.cursor()
	query = "SELECT airline_name FROM airline_staff WHERE username = '{}'"
	cursor.execute(query.format(username))
	airline_name = cursor.fetchone()[0]

	# Defaults will be showing all the upcoming flights operated by the airline he/she works for the next 1 year.
	query = """SELECT * FROM flight WHERE airline_name = '{}' AND departure_time BETWEEN NOW() AND date_add(NOW(), INTERVAL 1 year) ORDER BY departure_time"""
	cursor.execute(query.format(airline_name))
	flights = cursor.fetchall()
	cursor.close()
	
	return render_template('as_changeStatus.html', flights=flights, username=username, error=error)
@app.route('/changeStatus', methods=["POST"])
def changeStatus():
	username = session['username']
	data_index = int(request.form["data-index"])-1
	flight_num  = request.form.getlist("flight_num")[data_index]
	airline_name = request.form.getlist('airline_name')[data_index] 
	status = request.form.getlist('status')[data_index]
	error = None
	
	cursor = conn.cursor()	
	query = "SELECT airline_name FROM airline_staff WHERE username = '{}'"
	cursor.execute(query.format(username))
	airline_name = cursor.fetchone()[0]

	# Defaults will be showing all the upcoming flights operated by the airline he/she works for the next 1 year.
	query = """SELECT * FROM flight WHERE airline_name = '{}' AND departure_time BETWEEN NOW() AND date_add(NOW(), INTERVAL 1 year) ORDER BY departure_time"""
	cursor.execute(query.format(airline_name))
	flights = cursor.fetchall()

	query = """UPDATE flight SET status="{}" WHERE airline_name="{}" AND flight_num={};"""
	cursor.execute(query.format(status,airline_name,flight_num))
	conn.commit()
	cursor.close()
	#return render_template('as_changeStatus.html', flights=flights, username=username, error=error)
	return render_template('as_success.html', username=username, error=error)

@app.route('/addAirplane')
def addAirplaneLoad():
	username = session['username']
	error = None
	cursor = conn.cursor()
	query = "SELECT DISTINCT {} FROM airplane"
	cursor.execute(query.format("airline_name"))
	airlines = cursor.fetchall()
	
	cursor.close()
	return render_template('as_addAirplane.html', username=username, error=error, airlines=airlines, )

@app.route('/addAirplane',methods=["POST"])
def addAirplane():
	username = session['username']
	airline_name = request.form['airline_name'] # inputs
	seats = request.form['seats'] #

	cursor = conn.cursor()
	query = "SELECT airplane_id FROM airplane"
	cursor.execute(query)
	a_ids = cursor.fetchall()
	a_ids.sort()
	if len(a_ids) == 0:
		airplane_id = 1
	else:
		airplane_id = str(int(a_ids[-1][0]) + 1)
	
	query = """INSERT INTO `airplane` (`airline_name`,`airplane_id`,`seats`) 
  			VALUES ('{}','{}','{}');"""
	cursor.execute(query.format(airline_name,airplane_id,seats))
	conn.commit()
	cursor.close()
	error = None
	#return render_template('as_addAirplane.html', username=username, error=error)
	return render_template('as_success.html', username=username, error=error)


@app.route('/addAirport')
def loadAirports():
	username = session['username']
	error = None
	return render_template('as_addAirport.html', username=username, error=error)

@app.route('/addAirport',methods=["POST"])
def addAirport():
	username = session['username']
	airport_name = request.form['airport_name'] # inputs
	airport_city = request.form['airport_city'] #
	error = None	
	if airport_name=="" or airport_city=="":
		error = "Name or City cannot be empty!"
		return render_template('as_addAirport.html',username=username, error = error)
	cursor = conn.cursor()
	query = """ SELECT * FROM airport WHERE airport_name = "{}" """
	cursor.execute(query.format(airport_name))
	result = cursor.fetchone()
	if result:
		error = "This airport already exists"
		return render_template('as_addAirport.html',username=username, error = error)
	else:
		query = """INSERT INTO `airport` (`airport_name`,`airport_city`) 
				VALUES ("{}","{}");"""
		cursor.execute(query.format(airport_name,airport_city))
		conn.commit()
		cursor.close()
		#return render_template('as_addAirport.html', username=username, error=error)
		return render_template('as_success.html', username=username, error=error)

@app.route('/sViewBA')
def sViewBA():
	username = session['username']
	cursor = conn.cursor()
	query = """SELECT email FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff WHERE purchase_date 
			BETWEEN date_sub(NOW(), INTERVAL {}) and NOW() AND username = '{}' GROUP BY email ORDER BY COUNT(ticket_id) DESC LIMIT 5"""
	cursor.execute(query.format('1 month', username))
	data_month = cursor.fetchall()
	cursor.execute(query.format('1 year', username))
	data_year = cursor.fetchall()

	query = """SELECT email FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff WHERE purchase_date 
			BETWEEN date_sub(NOW(), INTERVAL 1 year) and NOW() AND username = '{}' GROUP BY email ORDER BY SUM(price) DESC LIMIT 5"""
	cursor.execute(query.format(username))
	data_year_com = cursor.fetchall()
	cursor.close()
	error = None
	return render_template('as_viewBA.html', username=username, data_month=data_month, data_year=data_year, data_year_com=data_year_com, error=error)

@app.route('/sViewCustomer')
def sViewCustomer():
	username = session['username']
	error = None
	is_top = True

	cursor = conn.cursor()
	query_1 = """ SELECT email FROM customer """
	cursor.execute(query_1)
	customers = cursor.fetchall()

	query = """SELECT customer_email FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE purchase_date 
			BETWEEN date_sub(NOW(), INTERVAL 1 year) and NOW() GROUP BY customer_email ORDER BY COUNT(ticket_id) DESC"""
	cursor.execute(query)
	top_customer = cursor.fetchone()[0]

	query = """SELECT * FROM flight WHERE flight_num IN (SELECT DISTINCT flight_num FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff 
			WHERE customer_email = '{}' AND username = '{}')"""
	cursor.execute(query.format(top_customer, username))
	flights = cursor.fetchall() # a list of all flights a particular Customer has taken only on that particular airline.
	cursor.close()

	return render_template('as_viewCustomer.html', is_top=is_top, username=username, top_customer=top_customer, customers=customers, flights=flights, error=error)
@app.route('/sViewCustomer', methods=["POST"])
def sViewCustomerSearch():
	customer = request.form.get('customer') # input
	print(customer)
	username = session['username']
	error = None
	is_top = True
	cursor = conn.cursor()
	query_1 = """ SELECT email FROM customer """
	cursor.execute(query_1)
	customers = cursor.fetchall()

	query = """SELECT customer_email FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE purchase_date 
			BETWEEN date_sub(NOW(), INTERVAL 1 year) and NOW() GROUP BY customer_email ORDER BY COUNT(ticket_id) DESC"""
	cursor.execute(query)
	top_customer = cursor.fetchone()[0]

	if top_customer != customer:
		is_top = False
	query = """SELECT * FROM flight WHERE flight_num IN (SELECT DISTINCT flight_num FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff 
			WHERE customer_email = '{}' AND username = '{}')"""
	cursor.execute(query.format(customer, username))
	flights = cursor.fetchall() # a list of all flights a particular Customer has taken only on that particular airline.
	cursor.close()
	print(is_top)
	return render_template('as_viewCustomer.html', is_top=is_top, username=username, top_customer=top_customer, customers=customers, flights=flights, error=error)


@app.route('/sViewReport')
def sViewReport():
	username = session['username']

	# To do: range of dates

	cursor = conn.cursor()
	query = """SELECT SUM(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff WHERE username = '{}'
			AND purchase_date BETWEEN date_sub(NOW(), INTERVAL 1 year) and NOW()"""
	cursor.execute(query.format(username))
	last_year = cursor.fetchone()[0]

	query = """SELECT SUM(price) FROM flight NATURAL JOIN ticket NATURAL JOIN purchases NATURAL JOIN airline_staff WHERE username = '{}' 
			AND purchase_date BETWEEN date_sub(NOW(), INTERVAL {} month) and date_sub(NOW(), INTERVAL {} month)"""
	bar_data = []
	for i in range(0,12):
		cursor.execute(query.format(username, str(i+1), str(i)))
		bar_data.append(cursor.fetchone()[0])
	cursor.close()

	last_month = bar_data[-1]
	data_date = None
	error = None
	return render_template('as_viewReport.html', username=username, data_date=data_date, last_year=last_year, last_month=last_month, bar_data=bar_data, error=error)

@app.route('/sViewReport',methods=["POST"])
def sViewReportSearch():
	username = session['username']

	# To do: range of dates
	start = request.form['start']
	end = request.form['end']
	cursor = conn.cursor()

	# Allow to specify a range of dates
	query = """SELECT SUM(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff WHERE username = '{}'
			AND purchase_date BETWEEN '{} 00:00:00' AND '{} 00:00:00'"""
	cursor.execute(query.format(username, start, end))
	data_date = cursor.fetchone()[0]

	cursor = conn.cursor()
	query = """SELECT SUM(price) FROM purchases NATURAL JOIN ticket NATURAL JOIN flight NATURAL JOIN airline_staff WHERE username = '{}'
			AND purchase_date BETWEEN date_sub(NOW(), INTERVAL 1 year) and NOW()"""
	cursor.execute(query.format(username))
	last_year = cursor.fetchone()[0]

	query = """SELECT SUM(price) FROM flight NATURAL JOIN ticket NATURAL JOIN purchases NATURAL JOIN airline_staff WHERE username = '{}' 
			AND purchase_date BETWEEN date_sub(NOW(), INTERVAL {} month) and date_sub(NOW(), INTERVAL {} month)"""
	bar_data = []
	for i in range(0,12):
		cursor.execute(query.format(username, str(i+1), str(i)))
		bar_data.append(cursor.fetchone()[0])
	cursor.close()

	last_month = bar_data[-1]
	error = None
	return render_template('as_viewReport.html', username=username, data_date=data_date, last_year=last_year, last_month=last_month, bar_data=bar_data, error=error)

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

@app.route('/sRevenue')
def sViewDestination():
	username = session['username']
	error = None
	return render_template('as_revenue.html', username=username, direct=direct, indirect=indirect, error=error)
@app.route('/logout')
def logout():
	if 'email' in session:
		session.pop('email')
	elif 'email_b' in session:
		session.pop('email_b')
	else:
		session.pop('username')
	return render_template('goodbye.html')
	
@app.route('/goodbye')
def goodbye():
	return redirect('/')
	
app.secret_key = 'some key that you will never guess'
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION

if __name__ == "__main__":
	app.run('127.0.0.1', 5010, debug = True)
