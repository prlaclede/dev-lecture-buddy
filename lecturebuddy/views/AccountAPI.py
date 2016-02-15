import psycopg2, psycopg2.extras, time, os, datetime, logging
from flask import (Flask, Blueprint, render_template, request, 
session, url_for, redirect)
from flask.ext.iniconfig import INIConfig
from lecturebuddy.modules import *


accountAPI = Blueprint('accountAPI', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@accountAPI.route('/register', methods=['GET', 'POST'])
def register():
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    admin = 0
    errorMessage = ""
    
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        adminCode = request.form['adminCode']
        
        if adminCode == ADMIN_CODE:
            admin = 1
            
        if password1 == password2 and password1 != "":
            if firstName != "" and lastName != "" and username != "":
                try:
                    #Insert Person Information
                    query = "SELECT username FROM person WHERE username = '%s'"
                    cur.execute(query % username)
                    results = cur.fetchall()
                    if not results:
                        try:
                            #Insert Person Information
                            query1 = "INSERT INTO person (firstname, lastname, admin, username, password) VALUES (%s, %s, %s, %s, crypt(%s, gen_salt('bf')))"
                            cur.execute(query1, (firstName, lastName, str(admin), username, password1))
                            print("executed query")
                            conn.commit()
                            if admin == 1:
                                directory = 'lecturebuddy/static/pictures/' + username
                                if not os.path.exists(directory):
                                    os.makedirs(directory)
                                #os.mkdir("static/pictures/" + username)
                            return redirect(url_for('.login', newUser=True))
                        except:
                            print("Error Registering new user")
                            errorMessage = "Error Registering"
                    else:
                        print("Username Is Already In Use")
                        errorMessage = "Username Is Already In Use"
                except:
                    print("Error Registering check user")
                    errorMessage = "Error Registering"
            else:
                print "Either firstName, lastName, or username was left empty"
                errorMessage = "Either First Name, Last Name, or Username Were Left Empty"
        else:
            print("Passwords Do Not Match")
            errorMessage = "Passwords Do Not Match"
        
    
    return render_template('register.html', error = errorMessage, admin=ADMIN_CODE)
    
@accountAPI.route('/login', defaults={'newUser': None}, methods=['GET', 'POST'])
@accountAPI.route('/login/<newUser>', methods=['GET', 'POST'])
def login(newUser):
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    errorMessage = ""
    successMessage = ""
    
    if (newUser):
        successMessage = "Registation Successful, Please login below."
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            query = "SELECT username, password, admin, personid FROM person WHERE username = %s AND password = crypt(%s, password)"
            cur.execute(query, (username, password))
            results = cur.fetchone()
            if results:
                session['username'] = results.get(0)
                session['admin'] = results.get(2)
                session['personid'] = results.get(3)
                if results[2]:
                    return redirect(url_for('adminAPI.homeAdmin'))
                else:
                    return redirect(url_for('studentAPI.homeStudent'))
            else:
                errorMessage = "Username or Password Incorrect."
        except:
            errorMessage = "Error On Login"
            print("Error On Login")
    return render_template('login.html', error = errorMessage, success = successMessage)
    
@accountAPI.route('/logout')
def logout():
    session.clear()
    return render_template('welcome.html')
