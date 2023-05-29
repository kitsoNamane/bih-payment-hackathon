from flask import Flask, flash, session, render_template, request, redirect, url_for
import requests


API_URL = "http://127.0.0.1:8000"

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    return "<p>Customer Home Page</p>"

@app.route("/registration/")
def customer_redistration():
    return "<p>Customer Registration</p>"

@app.route("/login/")
def customer_login():
    return "<p>Customer Login</p>"

@app.route("/admin/registration/", methods=("GET", "POST"))
def admin_redistration():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        payload = {
            "email": email,
            "password": password
        }
        res = requests.post(f"{API_URL}/admin/registration", json=payload)
        if res.status_code == 400:
            flash("user already registered")
        elif res.status_code != 200:
            flash("something went wrong, registration failed")
        else:
            return redirect(url_for("admin_login"))

    return render_template('auth/admin_register.html')

@app.route("/admin/login/", methods=("GET", "POST"))
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        payload = {
            "email": email,
            "password": password
        }
        res = requests.post(f"{API_URL}/admin/login", json=payload)
        if res.status_code == 401:
            flash("invalid credentials")
        elif res.status_code != 200:
            flash("something went wrong, registration failed")
        else:
            session.clear()
            session['token'] = res.text
            print(session['token'])
            return redirect(url_for("admin"))

    return render_template('auth/admin_login.html')

@app.route("/admin/")
def admin():
    return "<p>Admin Homepage</p>"
