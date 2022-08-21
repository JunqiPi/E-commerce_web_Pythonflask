from flask import Flask , redirect , render_template, request, url_for
#from formsubmission import gogetmygurumartRegistrationForm
import sqlite3 as sql
import re

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

@app.route('/',methods=['GET'])
def get_home():
    return render_template('Homepage.html')

@app.route('/login',methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/register',methods=['GET'])
def get_signup():
    return render_template('register.html')

@app.route('/personal/<email>/<fname>/<lname>/<gender>/<age>/<home>/<bill>',methods=['GET'])
def personal(email,fname,lname,gender,age,home,bill):
    if request.method=='GET':
        result=checkhome(home)
        zipcode=result[0][0]
        city=result[0][1]
        state=result[0][2]
        street=result[0][3]
        fourd=cred(email)
        return render_template('personal.html', email=email,fname=fname,lname=lname,gender=gender,age=age,bill=bill, zipcode=zipcode,state=state,street=street,city=city,credit=fourd[0][0])    

@app.route('/personal',methods=['POST'])
def personal_post():
     changepass(request.form['email'], request.form['old'],request.form['new'])
     return redirect(url_for('login_post'))

@app.route('/product',methods=['GET'])
def product_get():
    return render_template('product.html')

@app.route('/add',methods=['GET'])
def add_prod():
    result=getcate()
    return render_template('add.html',result=result)

def getcate():
    connection = sql.connect('nittany.db')
    cursor = connection.execute('SELECT DISTINCT category_name FROM Category ')
    return cursor.fetchall()

@app.route('/add',methods=['POST'])
def add_post():
    error=None
    result=additem(request.form['email'],request.form['title'],request.form['cate'],request.form['Pro_name'],request.form['Pro_des'],request.form['Price'],request.form['quan'])
    if(result==0):
        result=getcate()
        return render_template('add.html',error="This email dose not exit",result=result)
    return render_template('add.html')

def additem(email,title,cate,name,des,price,quan):
    connection = sql.connect('nittany.db')
    cursor = connection.execute('SELECT MAX(Listing_ID) FROM listing ')
    incid=cursor.fetchall()[0][0]
    incid=incid+1
    cursor = connection.execute('SELECT * FROM sellers WHERE seller_email=(?) ', (email,))
    if(len(cursor.fetchall())==0):
        return 0
    connection.execute('INSERT INTO listing (seller_email, Listing_ID, Category, Title, Product_Name, Product_Description, Price, Quantity,active) VALUES (?,?,?,?,?,?,?,?,true) ', (email,incid,cate,title,name,des,price,quan))
    connection.commit()
    return 1

@app.route('/product',methods=['POST'])
def product_post():
    if request.method=='POST':
        result=category(request.form['cate'])
        product=listin(request.form['cate'])
        return render_template('product.html',result=result,product=product)

@app.route('/vendor/<addr>/<email>/<bus>/<ser>',methods=['POST','GET'])
def vendor(addr,email,bus,ser):
    if request.method=='POST':
         changepass(request.form['email'], request.form['old'],request.form['new'])
         return redirect(url_for('login_post'))
    if request.method =='GET':
        home=checkhome(addr)
        zipcode=home[0][0]
        city=home[0][1]
        state=home[0][2]
        street=home[0][3]
        sell=items(email)
        off=offed(email)
        return render_template('vendor.html', off=off,sell=sell,email=email,addr=addr,bus=bus, ser=ser, zipcode=zipcode,state=state,street=street,city=city) 



@app.route('/vendor/offlist',methods=['POST'])
def venoff():
         off=None
         off=request.form['off']
         offlist(off)
         return redirect(url_for('login_post'))

@app.route('/seller/offlist',methods=['POST'])
def selloff():
         off=None
         off=request.form['off']
         offlist(off)
         return redirect(url_for('login_post'))

@app.route('/seller/<email>/<fname>/<lname>/<gender>/<age>/<home>/<bill>',methods=['POST','GET'])
def seller(email,fname,lname,gender,age,home,bill):
    if request.method=='POST':
         changepass(request.form['email'], request.form['old'],request.form['new'])
         return redirect(url_for('login_post'))
    if request.method =='GET':
        home=checkhome(home)
        zipcode=home[0][0]
        city=home[0][1]
        state=home[0][2]
        street=home[0][3]
        fourd=cred(email)
        sell=items(email)
        off=offed(email)
        return render_template('seller.html', off=off,sell=sell,email=email,fname=fname,lname=lname,gender=gender,age=age,bill=bill, zipcode=zipcode,state=state,street=street,city=city,credit=fourd[0][0]) 

@app.route('/login',methods=['POST'])
def login_post():
    error = None
    result = loginf(request.form['email'], request.form['password'])
    connection = sql.connect('nittany.db')
    cursor = connection.execute('SELECT vendor_email, Business_Name, Business_Address_ID, Customer_Service_Number FROM vendor, users WHERE email=(?) AND password = (?) AND vendor_email= (?)',(request.form['email'], request.form['password'], request.form['email'],))
    checkvender=cursor.fetchall()
    if(len(checkvender)!=0):
        return redirect(url_for('vendor',addr=checkvender[0][2],email=checkvender[0][0], bus=checkvender[0][1],ser=checkvender[0][3]))
    if len(result)!=0:
        connection = sql.connect('nittany.db')
        cursor = connection.execute('SELECT seller_email, first_name, last_name, gender, age, home_address_id, billing_address_id FROM sellers, buyers WHERE seller_email = (?) AND buyer_email = seller_email',(request.form['email'],))
        buyseller=cursor.fetchall()
        if(len(buyseller)!=0):
            return redirect(url_for('seller', email=buyseller[0][0], fname=buyseller[0][1],  lname=buyseller[0][2], gender=buyseller[0][3], age=buyseller[0][4], home=buyseller[0][5], bill=buyseller[0][6]))
        return redirect(url_for('personal', email=result[0][0], fname=result[0][1],  lname=result[0][2], gender=result[0][3], age=result[0][4], home=result[0][5], bill=result[0][6]))
    else:
        return render_template('login.html',error="The username or password is incorrect")

@app.route('/register',methods=['POST'])
def signup_post():
    error = None
    result = register_name(request.form['email'], request.form['password'])
    if result:
        return redirect('/')
    else:
        error = 'Username or password Wrong'

def offlist(list):
    connection = sql.connect('nittany.db')
    connection.execute('UPDATE listing SET active=false WHERE Listing_ID=(?)', (list,))
    connection.commit()

def category(cate):
    connection = sql.connect('nittany.db')
    cursor = connection.execute('SELECT category_name FROM Category WHERE parent_category = (?) COLLATE NOCASE', (cate,))
    return cursor.fetchall()

def items(email):
    connection = sql.connect('nittany.db')
    cursor = connection.execute('SELECT Listing_ID, Category, Title, Product_Name, Product_Description, Price, Quantity FROM listing WHERE seller_email=(?) AND active=true COLLATE NOCASE', (email,))
    return cursor.fetchall()

def offed(email):
    connection = sql.connect('nittany.db')
    cursor = connection.execute('SELECT Listing_ID, Category, Title, Product_Name, Product_Description, Price, Quantity FROM listing WHERE seller_email=(?) AND active=false COLLATE NOCASE', (email,))
    return cursor.fetchall()

def listin(cate):
    connection = sql.connect('nittany.db')
    cursor = connection.execute('SELECT DISTINCT seller_email, Listing_ID, Category, Title, Product_Name, Product_Description, Price, Quantity FROM listing WHERE Category=(?) COLLATE NOCASE AND active=true COLLATE NOCASE', (cate,))
    return cursor.fetchall()

def loginf(user_email,user_pass):
    connection = sql.connect('nittany.db')
    cursor = connection.execute('SELECT email, first_name, last_name, gender, age, home_address_id, billing_address_id FROM buyers, users WHERE email=(?) AND password = (?) AND buyer_email= email', (user_email,user_pass))

    return cursor.fetchall()

def checkhome(home):
    connection = sql.connect('nittany.db')
    cursor = connection.execute('SELECT Z.zipcode,Z.city,Z.state_id,A.street_name FROM address A, zip Z WHERE address_ID= (?) AND A.zipcode=Z.zipcode', (home,))
    return cursor.fetchall()

def changepass(email,old,new):
    connection = sql.connect('nittany.db')
    connection.execute('UPDATE users SET password=(?) WHERE email=(?) AND password=(?)', (new,email,old))
    connection.commit()

def cred(email):
    connection = sql.connect('nittany.db')
    cursor = connection.execute('SELECT SUBSTR(credit_card_num,(length(credit_card_num)-3),4) FROM card WHERE  Owner_email=(?)', (email,))
    return cursor.fetchall()

def register_name(user_email,user_pass):
    connection = sql.connect('nittany.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(email CHAR(30) PRIMARY KEY NOT NULL, password CHAR(30) NOT NULL);')
    connection.commit()
    connection.execute('INSERT INTO users (email, password) VALUES (?,?) ', (user_email,user_pass))
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()

if __name__ == "__main__":
    app.debug=True
    app.run()
    dump()


