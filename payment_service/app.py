import datetime
from hashlib import md5
from flask import Flask, redirect, request
import re

import requests
app = Flask(__name__)

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







 
# http://127.0.0.1:5000/?reference=pako&amount=1000&serviceid=sea&email=chalebgwa.bc@gmail.com

