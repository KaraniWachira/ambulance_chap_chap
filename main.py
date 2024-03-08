import os
from flask import Flask, request
import africastalking

username = ''
api_key = ''
africastalking.initialize(username, api_key)
sms = africastalking.SMS;


def sending(recipients, message):
  # Set the numbers in international format
  try:
      response = sms.send(message, [recipients])
      print("Hello !")
      print (response)
  except Exception as e:
      print (f'Houston, we have a problem: {e}')

app = Flask(__name__)

# dictionary for storing the ambulance numbers
number = {
    "1*1": "",
    "1*2": "",
    "1*3": "",
    "2*1": "",
    "2*2": "",
    "2*3": ""
}

# *384*123#
@app.route('/')
def index():
  return 'Ambulance Chap Chap!'

@app.route("/ussd", methods=['POST'])
def ussd():
  # Read the variables sent via POST from our API
  session_id = request.values.get("sessionId", None)
  serviceCode = request.values.get("serviceCode", None)
  phone_number = request.values.get("phoneNumber", None)
  text = request.values.get("text", "default")

  if text == '':
    # This is the first request. Note how we start the response with CON
    #response  = "CON Welcome To Ambulance Chap Chap! \n"
    response = "CON Select Nearest Town from Emergency occurence  \n"
    response += "1. Nyeri Town \n"
    response += "2. Nyaribo \n"
    print(response)

  elif text == '1':
    # Business logic for first level response
    response = "CON Nearest Ambulance in Nyeri Town\n"
    response += "1. St Johns Ambulance Kenya \n"
    response += "2. Red Cross Kenya \n "
    response += "3. AAR Ambulances\n "

  elif text == '2':
    response = "CON Nearest Ambulance in Nyaribo\n"
    response += "1. St Rita Ambulance Kenya \n"
    response += "2. Nyeri PGH Ambulance \n "
    response += "3. Outspan Ambulances\n "

    # This is a terminal request. Note how we start the response with END
    #response = "END Your phone number is " + phone_number
  elif text == '1*1':
    # This is a second level response where the user selected 1 in the first instance
    # print("hello")
    # print(number[text])
    sending(recipients = number[text], message = f"Emergency request by {phone_number} has been directed to you. Please avail to their location")
    response = " END St Johns Ambulance have been alerted"

  elif text == '1*2':
    # This is a second level response where the user selected 2 in the first instance
    sending(recipients = number[text], message = f"Emergency request by {phone_number} has been directed to you. Please avail to their location")
    response = "END RedCross Ambulance have been alerted"

  elif text == '1*3':
    # This is a second level response where the user selected 3 in the first instance
    sending(recipients = number[text], message = f"Emergency request by {phone_number} has been directed to you. Please avail to their location")
    response = "END AAR Ambulances have been alerted"

  elif text == '2*1':
    # This is a second level response where the user selected 1 in the second instance
    sending(recipients = number[text], message = f"Emergency request by {phone_number} has been directed to you. Please avail to their location")
    response = "END St Rita Ambulance Kenya have been alerted"

  elif text == '2*2':
    # This is a second level response where the user selected 2 in the second instance
    sending(recipients = number[text], message = f"Emergency request by {phone_number} has been directed to you. Please avail to their location")
    response = "END Nyeri PGH Ambulance have been alerted"

  elif text == '2*3':
    # This is a second level response where the user selected 3 in the second instance
    sending(recipients = number[text], message = f"Emergency request by {phone_number} has been directed to you. Please avail to their location")
    response = "END Outspan Ambulances have been alerted"

    # This is a terminal request. Note how we start the response with END
    #response       = "END Your account number is " + accountNumber

  else:
    response = "END Invalid choice"

  # Send the response back to the API
  return response


app.run(host='0.0.0.0', port=81)





