from flask import Flask, render_template, request, redirect, url_for

app=Flask(__name__)

@app.route("/")
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        us="yogi"
        pw="password"
        if username==us and password==pw:
            return render_template("index.html",msg=us)
    return render_template("home.html")

@app.route("/register")
def register():
    return render_template("register.html")
