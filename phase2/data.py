import sqlite3 as sql
import csv

#user
def user():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('CREATE TABLE users(email CHAR(30) PRIMARY KEY NOT NULL, password CHAR(30) NOT NULL);')
	content = csv.reader(open("Users.csv"))

	insert='INSERT INTO users (email, password) VALUES (?,?) '
	cursor.executemany(insert,content)
	connection.commit()

#buyers
def Buyers():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('CREATE TABLE buyers(buyer_email CHAR(30) PRIMARY KEY NOT NULL REFERENCES users(email), first_name TEXT, last_name TEXT, gender TEXT, age INT, home_address_id TEXT, billing_address_id TEXT);')
	content = csv.reader(open("Buyers.csv"))

	insert='INSERT INTO buyers(buyer_email, first_name, last_name, gender, age, home_address_id, billing_address_id) VALUES (?,?,?,?,?,?,?) '
	cursor.executemany(insert,content)
	cursor.execute("SELECT * FROM buyers")

	data = cursor.fetchall()
	for row in data:
		print(row)

	connection.commit()

#Sellers
def Sellers():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('CREATE TABLE sellers(seller_email CHAR(30) PRIMARY KEY NOT NULL REFERENCES buyers(buyer_email) REFERENCES vendor(vendor_email), routing_number INT, account_number INT, balance INT);')
	content = csv.reader(open("Sellers.csv"))

	insert='INSERT INTO sellers(seller_email, routing_number, account_number, balance) VALUES (?,?,?,?) '
	cursor.executemany(insert,content)
	cursor.execute("SELECT * FROM sellers")

	data = cursor.fetchall()
	for row in data:
		print(row)

	connection.commit()
#Credit_Cards
def Credit_Cards():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('CREATE TABLE card(credit_card_num INT PRIMARY KEY NOT NULL, card_code INT, expire_month TEXT, expire_year TEXT, card_type TEXT, Owner_email TEXT REFERENCES buyers(buyer_email));')
	content = csv.reader(open("Credit_Cards.csv"))

	insert='INSERT INTO card(credit_card_num, card_code, expire_month, expire_year, card_type, Owner_email) VALUES (?,?,?,?,?,?) '
	cursor.executemany(insert,content)
	cursor.execute("SELECT * FROM card")

	data = cursor.fetchall()
	for row in data:
		print(row)

	connection.commit()

#Address
def addr():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('CREATE TABLE address(address_ID INT NOT NULL PRIMARY KEY , zipcode, street_num, street_name, FOREIGN KEY(address_ID) REFERENCES buyers(home_address_id) FOREIGN KEY(address_ID) REFERENCES buyers(billing_address_id) FOREIGN KEY(address_ID) REFERENCES vendor(Business_Address_ID));')
	content = csv.reader(open("Address.csv"))

	insert='INSERT INTO address(address_ID, zipcode, street_num, street_name) VALUES (?,?,?,?) '
	cursor.executemany(insert,content)
	cursor.execute("SELECT * FROM address")

	data = cursor.fetchall()
	for row in data:
		print(row)

	connection.commit()

#Zipcode_Info
def zipcode():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('CREATE TABLE zip(zipcode INT NOT NULL PRIMARY KEY, city TEXT, state_id CHAR, population INT, density REAL, county_name TEXT, timezone TEXT);')
	content = csv.reader(open("Zipcode_Info.csv"))

	insert='INSERT INTO zip(zipcode, city, state_id, population, density, county_name, timezone) VALUES (?,?,?,?,?,?,?) '
	cursor.executemany(insert,content)
	cursor.execute("SELECT * FROM zip")

	data = cursor.fetchall()
	for row in data:
		print(row)

	connection.commit()

#Local_Vendors
def vendor():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('CREATE TABLE vendor(vendor_email CHAR(30) PRIMARY KEY NOT NULL REFERENCES sellers(seller_email), Business_Name TEXT, Business_Address_ID CHAR(50), Customer_Service_Number CHAR(30));')
	content = csv.reader(open("Local_Vendors.csv"))

	insert='INSERT INTO vendor(vendor_email, Business_Name, Business_Address_ID, Customer_Service_Number) VALUES (?,?,?,?) '
	cursor.executemany(insert,content)
	cursor.execute("SELECT * FROM vendor")

	data = cursor.fetchall()
	for row in data:
		print(row)

	connection.commit()

#Categories
def cate():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('CREATE TABLE Category(parent_category TEXT, category_name TEXT PRIMARY KEY NOT NULL);')
	content = csv.reader(open("Categories.csv"))

	insert='INSERT INTO Category(parent_category, category_name) VALUES (?,?) '
	cursor.executemany(insert,content)
	cursor.execute("SELECT * FROM Category")

	data = cursor.fetchall()
	for row in data:
		print(row)

	connection.commit()

#Product_Listings
def List():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('CREATE TABLE listing(seller_email TEXT, Listing_ID INT PRIMARY KEY NOT NULL, Category TEXT, Title TEXT, Product_Name TEXT, Product_Description TEXT, Price MONEY, Quantity INT, UNIQUE(seller_email,Listing_ID));')
	content = csv.reader(open("Product_Listing.csv"))

	insert='INSERT INTO listing(seller_email, Listing_ID, Category, Title, Product_Name, Product_Description, Price, Quantity) VALUES (?,?,?,?,?,?,?,?) '
	cursor.executemany(insert,content)
	cursor.execute("SELECT * FROM listing")

	data = cursor.fetchall()
	for row in data:
		print(row)

	connection.commit()

#Orders
def order():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('CREATE TABLE orders(Transaction_ID INT PRIMARY KEY NOT NULL, seller_email TEXT, Listing_ID INT, Buyer_Email TEXT, order_date TEXT, Quantity INT, Payment INT, UNIQUE(seller_email,Listing_ID) );')
	content = csv.reader(open("Orders.csv"))

	insert='INSERT INTO orders(Transaction_ID, seller_email, Listing_ID, Buyer_Email, order_date, Quantity, Payment) VALUES (?,?,?,?,?,?,?) '
	cursor.executemany(insert,content)
	cursor.execute("SELECT * FROM orders")

	data = cursor.fetchall()
	for row in data:
		print(row)

	connection.commit()

#Reviews
def review():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('CREATE TABLE review(buyer_email TEXT , seller_email TEXT, Listing_ID INT PRIMARY KEY NOT NULL, Review_Desc TEXT, UNIQUE(seller_email,Listing_ID));')
	content = csv.reader(open("Reviews.csv"))

	insert='INSERT INTO review(buyer_email, seller_email, Listing_ID, Review_Desc) VALUES (?,?,?,?) '
	cursor.executemany(insert,content)
	cursor.execute("SELECT * FROM review")

	data = cursor.fetchall()
	for row in data:
		print(row)

	connection.commit()

#Rating
def rating():
	connection =sql.connect("nittany.db")
	cursor = connection.cursor()

	cursor.execute('CREATE TABLE rating(buyer_email TEXT,  seller_email TEXT, order_date TEXT, Rating REAL, Rating_Desc TEXT, FOREIGN KEY(buyer_email) REFERENCES review(buyer_email));')
	content = csv.reader(open("Ratings.csv"))

	insert='INSERT INTO rating(buyer_email,  seller_email, order_date, Rating, Rating_Desc) VALUES (?,?,?,?,?) '
	cursor.executemany(insert,content)

	cursor.execute("SELECT * FROM rating")

	data = cursor.fetchall()
	for row in data:
		print(row)

	connection.commit()


user()
Buyers()
Sellers()
Credit_Cards()
addr()
zipcode()
vendor()
cate()
List()
order()
review()
rating()



