import sqlite3
from datetime import datetime
from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime('%A, %B %d, %Y %I:%M %p')

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect('signature.db')
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM signatures")
    if request.method == "POST":
        signature = request.form.get("signature")
        if check_for_profanity(signature):
            return render_template("index.html", data=data)
        elif signature and len(signature) <= 16:
            cursor.execute("INSERT INTO signatures (signature, time) VALUES(?, ?)", (signature, datetime.now().date()))
            conn.commit()
            data = cursor.execute("SELECT * FROM signatures")
    return render_template("index.html", data=data)

def check_for_profanity(signature):
    with open("static/profanity_en.csv", "r", newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            for cell in row:
                if signature.lower() in cell.lower():
                    return True
    return False

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/CS50")
def CS50():
    return render_template("CS50.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")

