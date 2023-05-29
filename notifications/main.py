#from fastapi import FastAPI, HTTPException
from twilio.rest import Client
import random

app = FastAPI()

# Twilio credentials
account_sid = "AC785cfddd528b3b3cd45d660b598c8496"
auth_token = "3fa502d2e8e2d4c130178d1df4060c6e"
twilio_phone_number = "+13156936980"

client = Client(account_sid, auth_token)




@app.post("/send_otp")
def send_otp(phone_number: str):
    otp = generate_otp()
    message_body = f"Your OTP is: {otp}"

    try:
        client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=phone_number
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send OTP")

    return {"message": "OTP sent successfully"}


@app.post("/send_payment_confirmation/{phone_number}")
def send_payment_confirmation(phone_number: str):
    message_body = "Your payment has been successfully processed."

    try:
        client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=phone_number
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send payment confirmation")

    return {"message": "Payment confirmation sent successfully"}


@app.post("/notify_new_charges/{phone_number}")
def notify_new_charges(phone_number: str):
    message_body = "You have new charges/fees to pay."

    try:
        client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=phone_number
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send new charges notification")

    return {"message": "New charges notification sent successfully"}


import requests

url = 'http://127.0.0.1:8000/send_otp'
data = {
    'phone_number': '+26772159011'
}

response = requests.post(url, json=data)

# Check the response status code
if response.status_code == 200:
    print('OTP sent successfully')
else:
    print('Failed to send OTP') put your code in here
