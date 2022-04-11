from flask import Flask, render_template, redirect, request
from libs.libs import *

app = Flask(__name__)

# user details
name = pwd = "default"
is_valid = False

@app.route("/")
def index():

    if not is_valid:
        return redirect("/login")
        
    return render_template("index.html")
    

@app.route("/login", methods = ["GET", "POST"])
def login():
    
    global name,pwd
    name = request.form.get("name", "default")
    pwd = request.form.get("pwd", "default")
    
    rec = Record(name, pwd)
    login_message = rec.validate()

    global is_valid
    is_valid = rec.is_auth_valid

    if is_valid:
        return redirect("/")
    return render_template("login.html", message = login_message)

@app.route("/dslab", methods = ["GET", "POST"])
def dslab():
    if not is_valid:
        return redirect("/login")
    
    return render_template("dslab.html", records = DictReader(open("files/dslab.csv")))