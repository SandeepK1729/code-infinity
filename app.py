from flask import Flask, render_template, redirect
from csv import DictReader

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    # return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dslab", methods = ["GET", "POST"])
def dslab():
    return render_template("dslab.html", records = DictReader(open("files/dslab.csv")))