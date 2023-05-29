from flask import Flask, flash, session, render_template, request, redirect, url_for
import requests
import datetime
import re
from hashlib import md5

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
            return redirect(url_for("admin"))

    return render_template('auth/admin_login.html')

@app.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("admin_login"))

@app.route("/admin/")
def admin():
    return render_template('admin.html')

def append_base_url_to_html(html_string, base_url):
    base_tag = f'<base href="{base_url}">'
    modified_html = re.sub(r"<head[^>]*>", lambda m: m.group() + base_tag, html_string)
    return modified_html

@app.route("/pay", methods=["GET"])
def initiatePay():
    url = "https://secure.paygate.co.za/payweb3/initiate.trans"
    encryptionKey = "secret"

    PAYGATE_ID = "10011072130"
    # extract the reference from the request
    REFERENCE = request.args.get("reference")
    AMOUNT = request.args.get("amount")
    SERVICEID = request.args.get("serviceid")
    EMAIL = request.args.get("email")

    # generate a unique transaction reference
    TRANSACTION_DATE = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LOCALE = "en-za"
    COUNTRY = "ZAF"
    
    # generate reference using the reference and the transaction date + serviceid
    REFERENCE = f"{REFERENCE}_{TRANSACTION_DATE}_{SERVICEID}"

    payload = {'PAYGATE_ID': '10011072130',
    'REFERENCE': REFERENCE,
    'AMOUNT': AMOUNT,
    'CURRENCY': 'BWP',
    'RETURN_URL': 'https://my.return.url/page',
    'TRANSACTION_DATE': TRANSACTION_DATE,
    'LOCALE': 'en-tn',
    'COUNTRY': 'BWA',
    'NOTIFY_URL': 'https://my.notify.url/page',
    'EMAIL': EMAIL,
    }

    # data_string 
    data_string = ''.join(str(value) for value in payload.values())
    # generate the checksum
    CHECKSUM = md5((data_string+encryptionKey).encode()).hexdigest()

    payload["CHECKSUM"] = CHECKSUM
    
    try: 
        response = requests.request("POST", url, data=payload,)
        payload=response.text
        pairs = payload.split("&")
        map = {}
        for pair in pairs:
            parts = pair.split("=")
            key = parts[0]
            value = parts[1]
            map[key] = value
      
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = "https://secure.paygate.co.za/payweb3/process.trans"
        response = requests.request("POST", url, headers=headers, data=map)
        return append_base_url_to_html(response.text, "https://secure.paygate.co.za/payweb3/")
    except Exception as e:
        print(e)
    return "Something went wrong, please try again later"
   
@app.route("/notify")
def notify():
    status = request.body.get("TRANSACTION_STATUS")
    # save request body to database here
    if(status == "1"):
        return redirect("/success")
    else: 
        return redirect("/failed")
    

@app.route("/success")
def success():
    return "Payment was successful"

@app.route("/failed")
def failed():
    return "Payment was unsuccessful"


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=6000, debug=True)





 
# http://127.0.0.1:5000/?reference=pako&amount=1000&serviceid=sea&email=chalebgwa.bc@gmail.com

