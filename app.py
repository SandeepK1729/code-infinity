from sqlite3 import Timestamp
from flask import Flask, render_template, redirect, request
from csv import DictReader
from datetime import datetime

app = Flask(__name__)

class Record:
    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        self.is_auth_valid = False
        self.login_message = ""

    def validate(self):
        if name != "default" and pwd != "default":
            # verification of credentials
            with open("files/data.csv") as file:
                records = DictReader(file)
                for record in records:
                    if name == record["name"] and pwd == record["pwd"]:
                        self.is_auth_valid = True
                        break
                else:
                    self.login_message = "Invalid Credentials"
            # history
            with open("files/history.csv","a") as file:
                time_stamp = datetime.now().strftime("%H:%M:%S %d/%m/%y")
                file.write(f"{name},{pwd},{time_stamp},{self.is_auth_valid}\n")
            
            
        elif name != "default" or pwd != "default":
            self.login_message = "Invalid Credentials"

        return self.login_message

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