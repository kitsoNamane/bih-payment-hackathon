from hashlib import md5
from flask import Flask, Request
from flask import request
import urllib.parse

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World</p>"

@app.route("/initiate")
def initiatePayment():
    secret = 'secret'
    payGateID = '10011072130'
    reference = '1'
    amount = '100.00'
    currency = 'ZAR'
    returnUrl = 'http://localhost:5000/return'
    cancelUrl = 'http://localhost:5000/cancel'
    notifyUrl = 'http://localhost:5000/notify'
    transactionDate = '2019-05-28 12:00:00'
    locale = 'en-za'
    country = 'ZAF'
    email = 'chalebgwa.bc@gmail.com'

    data = {
        'PAYGATE_ID': payGateID,
        'REFERENCE': reference,
        'AMOUNT': amount,
        'CURRENCY': currency,
        'RETURN_URL': returnUrl,
        'TRANSACTION_DATE': transactionDate,
        'LOCALE': locale,
        'COUNTRY': country,
        'EMAIL': email,
    }
    print(data)
    
    # implode data
    implodeData = ''
    for key in data:
        implodeData += data[key]
    
    # hash data with secret
    checksum = md5((implodeData + secret).encode('utf-8')).hexdigest()

    # add checksum to data
    data['CHECKSUM'] = checksum

    body = urllib.parse.urlencode(data).encode('utf-8')

    # Send the HTTP request
    url = 'https://secure.paygate.co.za/payweb3/initiate.trans'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': str(len(body)),
    }

    request = Request()

    response = request.post(url, body, headers)

    try:
        response = urllib.request.urlopen(url, body, headers).read()
        print(response)
    except urllib.error.HTTPError as e:
        print(e.code)
     


    return data 
