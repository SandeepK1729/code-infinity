from datetime import datetime
from flask import Flask, render_template, redirect, request
from libs.libs import *

app = Flask(__name__)

# user details
username = pwd = "default"
is_valid = False

@app.route("/")
def index():
    # if datetime.now().strftime("%H") == "23":
      #  Record("","").relay()
    if not is_valid:
        return redirect("/login")
        
    return render_template("index.html")
    

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method != "POST":
        return render_template("login.html", message = "")
    global username,pwd, is_valid
    username = request.form.get("username", "default")
    pwd = request.form.get("pwd", "default")
    
    rec = Record(username, pwd)
    is_valid = rec.validate()
    if is_valid:
        return redirect("/")
    return render_template("login.html", message = rec.login_message)

@app.route("/dslab", methods = ["GET", "POST"])
def dslab():
    if not is_valid:
        return redirect("/login")
    
    return render_template("dslab.html", records = DictReader(open("files/dslab.csv")))

@app.route("/register", methods = ["POST", "GET"])
def register():
    username = request.form.get("username", "default")
    mail = request.form.get("mail", "default")
    pwdrepeat = request.form.get("pwdrepeat", "default")
    name = request.form.get("name", "default")
    pwd = request.form.get("pwd", "default")

    if pwd != pwdrepeat:
        return render_template("register.html", message = "Password doesn't match")

    rec = Record(username, pwd, name, mail) 
    if not (rec.validate() or rec.is_auth_default or rec.is_exist):
        rec.register_new()
        return redirect("/login")
    elif rec.is_auth_default:
        return render_template("register.html", message = "")
    return render_template("register.html", message = "Account Credentials already exit, try to login")
    