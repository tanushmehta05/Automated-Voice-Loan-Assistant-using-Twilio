from twilio.rest import Client

ACCOUNT_SID = "" #add your own details please
AUTH_TOKEN = ""
TWILIO_NUMBER = ""
TO_NUMBER = ""  

client = Client(ACCOUNT_SID, AUTH_TOKEN)

call = client.calls.create(
    to=TO_NUMBER,
    from_=TWILIO_NUMBER,
    url="https://f07198042bac.ngrok-free.app/voice"
)

print(f"Call initiated, SID: {call.sid}")
