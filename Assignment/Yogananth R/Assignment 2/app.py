from flask import Flask, render_template, request, redirect, url_for
import ibm_db
from markupsafe import escape

conn=imb_db.connect("")

app=Flask(__name__)


@app.route("/")
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        sqll= f"SELECT username, password from user_login where username= '{escape(username)}'"
        stmt=ibm_db.exec_immediate(conn,sqll)
        dictionary=ibm_db.fetch_assoc(stmt)
        while dictionary != False:
            db_username=dictionary["username"]
            db_password=dictionary["password"]
            dictionary=ibm_db.fetch_assoc(stmt)

        
        if username==db_username and password==db_password:
            return render_template("index.html",msg=username)
        else:
            return render_template("login.html",msg="Login Invalid")
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")
