from flask import Flask,render_template,request
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="05112003", 
    database="login"
)
cursor = mydb.cursor()

@app.route('/')
def register_page():
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def register():
    fname = request.form['firstname']
    lname = request.form['lastname']
    email = request.form['email']
    uname = request.form['username']
    passwd = request.form['password']
    cpasswd = request.form['cpassword']

    if passwd != cpasswd:
        return "Password & Confirm Password do not match!"

    # Insert data into database
    query = "INSERT INTO users(firstname, lastname, email, username, password) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(query, (fname, lname, email, uname, passwd))
    mydb.commit()

    return "Registration Successful! <br><a href='/login'>Go to Login</a>"

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/logincheck', methods=['POST'])
def logincheck():
    uname = request.form['username']
    passwd = request.form['password']

    # Check in database
    query = "SELECT firstname, lastname, email, username FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (uname, passwd))
    user = cursor.fetchone()

    if user:
        # user = (firstname, lastname, email, username)
        return render_template("profile.html", user=user)
    else:
        return "Invalid Username or Password! <br><a href='/login'>Try Again</a>"

if __name__ == '__main__':
    app.run(debug=True)
