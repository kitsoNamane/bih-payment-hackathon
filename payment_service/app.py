import datetime
from hashlib import md5
from flask import Flask
import urllib.parse
from urllib import request, parse
import re

import requests
app = Flask(__name__)

def append_base_url_to_html(html_string, base_url):
    base_tag = f'<base href="{base_url}">'
    modified_html = re.sub(r"<head[^>]*>", lambda m: m.group() + base_tag, html_string)
    return modified_html

@app.route("/")
def initiatePay():
    url = "https://secure.paygate.co.za/payweb3/initiate.trans"

    payload = {'PAYGATE_ID': '10011072130',
    'REFERENCE': 'pgtest_123456789',
    'AMOUNT': '3299',
    'CURRENCY': 'ZAR',
    'RETURN_URL': 'https://my.return.url/page',
    'TRANSACTION_DATE': '2018-01-01 12:00:00',
    'LOCALE': 'en-za',
    'COUNTRY': 'ZAF',
    'EMAIL': 'customer@paygate.co.za',
    'CHECKSUM': '59229d9c6cb336ae4bd287c87e6f0220'}
    files=[

    ]

    try: 
        response = requests.request("POST", url, data=payload, files=files)
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
   
     


