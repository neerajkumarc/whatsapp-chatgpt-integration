from flask import Flask, request
import os
from twilio.twiml.messaging_response import MessagingResponse

my_secret = os.environ['TOKEN']
import openai

openai.api_key = my_secret


def getResults(question):
  completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{
                                              "role": "user",
                                              "content": f"{question}"
                                            }])
  return completion.choices[0].message


app = Flask(__name__)


@app.route("/")
def home():
  return "Integrating Chatgpt to Whatsapp"


@app.route('/bot', methods=['POST'])
def bot():
  incoming_msg = request.values.get('Body', '').lower()
  resp = MessagingResponse()
  msg = resp.message()
  data = getResults(incoming_msg)
  msg.body(data["content"])
  return str(resp)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)