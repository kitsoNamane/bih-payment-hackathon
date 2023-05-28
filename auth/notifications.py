from random import randint
from datetime import datetime
from twilio.rest import Client


ACCOUNT_SID = "AC785cfddd528b3b3cd45d660b598c8496"
AUTH_TOKEN = "3fa502d2e8e2d4c130178d1df4060c6e"
TWILIO_PHONE_NUMBER = "+13156936980"


def generate_otp():
    return str(randint(100000, 999999))


def create_sms_client() -> Client:
   return Client(ACCOUNT_SID, AUTH_TOKEN) 

def whitelist_phone_number(client: Client, phone_number: int):
    client.validation_requests.create(
      friendly_name='My Home Phone Number',
      phone_number=f"+267{phone_number}"
   )

def send_top(client: Client, phone_number: int):
   message = f"Your OTP is: {generate_otp()} do not share it with anyone"

   client.messages.create(
         body=message,
         to=f"+267{phone_number}",
         from_=TWILIO_PHONE_NUMBER
   )

def confirm_payment(client: Client, service: str, amount: float, paid_date: datetime, phone_number: int):
   message = f"Your payment for {service} of amout {amount} has been successfully paid on {paid_date}"
   client.messages.create(
         body=message,
         to=f"+267{phone_number}",
         from_=TWILIO_PHONE_NUMBER
   )

def notify_new_charge(client: Client, service: str, amount: float, due_date: datetime, phone_number: int):
   message = f"You have a outstanding payments for {service} of amout {amount}. Please pay before {due_date} to avoid further penalties"
   client.messages.create(
         body=message,
         to=f"+267{phone_number}",
         from_=TWILIO_PHONE_NUMBER
   )
