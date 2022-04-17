from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from libs.libs import *


app = Flask(__name__)

# user details
username = pwd = "default"
is_valid = False
status = ""
# session config
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def is_logged_in(): 
    user = session.get("name", "newbie")
    states = ["newbie", "verified"]
    return not (user in states or user == None )
# mail control route
@app.route("/")
def index():
    if not is_logged_in():
        return redirect("/login")
        
    return render_template("index.html")

""" sc harsh l1
@app.route("/harsh-L1")
def harsh_L1():
    render_"""

# account verification route  
@app.route("/account-verification", methods = ["GET"])
def verification():
    code = request.args.get("code")
    
    if Record.verify_mail(code):
        session["name"] = "verified"
        return render_template("verify.html", message = "Your Account Verified, ", link = "/login", word = "login")
    else:
        return render_template("verify.html", message = "Your Account not found, ", link = "/register", word = "register again")

# login route
@app.route("/login", methods = ["GET", "POST"])
def login():
    if is_logged_in():
        return redirect("/")
    if request.method == "GET" and session.get("name"):

        if session["name"] == "newbie":
            return render_template("login.html", message = "Activation link will be sent to your mail ID")
        elif session["name"] == "verified":
            return render_template("login.html", message = "Your account verified, login now")
        elif session["name"] == None:
            return render_template("login.html", message = "Your Logged out, login now")
        elif session["name"]:
            return redirect("/")

    global username,pwd, is_valid
    username = request.form.get("username", "default")
    pwd = request.form.get("pwd", "default")
    
    rec = Record(username, pwd)
    is_valid = rec.validate()
    if is_valid:
        session['name'] = username
        return redirect("/")
    return render_template("login.html", message = rec.login_message)

# logout route
@app.route("/logout")
def logout():
    session["name"] = None
    # print(session.get("name", "newbie"))
    return redirect("/")
# DS route
@app.route("/dslab", methods = ["GET", "POST"])
def dslab():
    if not is_logged_in():
        return redirect("/login")
    
    return render_template("dslab.html", records = DictReader(open("files/dslab.csv")))    

# register route
@app.route("/register", methods = ["POST", "GET"])
def register():
    if is_logged_in():
        return redirect("/")

    if request.method != "POST":
        return render_template("register.html", message = "")

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
        session["name"] = "newbie"
        return redirect("/login")
    elif rec.is_auth_default:
        return render_template("register.html", message = "")
    return render_template("register.html", message = rec.register_message)
    