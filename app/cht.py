import telegram

from logging import DEBUG
from flask import Flask, request
from pymessenger import Bot
from wit import Wit
import app.mmodule as mmodule

PAGE_ACCESS_TOKEN = '***REMOVED***'
Wit_ACCESS_TOKEN = '***REMOVED***'
VERIFICATION_TOKEN = 'Token'


bot = Bot(PAGE_ACCESS_TOKEN)


app = Flask(__name__)


# ---------------------------------------TEl
import os


TOKEN = os.environ['TOKEN']




tbot = telegram.Bot(token=TOKEN)

@app.route('/tele', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), tbot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    msg = update.message.text.encode('utf-8').decode()
    
    tbot.sendMessage(chat_id=chat_id, text=wittel(msg), reply_to_message_id=msg_id)
    
    return 'ok'


def wittel(text):
    client = Wit(Wit_ACCESS_TOKEN)
    resp = client.message(text)

    if len(resp.get('intents')) > 0:
        intent = resp.get('intents')[0].get('name')
        entity = list(resp.get('entities').values())[0][0].get('body')
        message = mmodule.main_function(intent, entity)
    else:
        message = "I'm not sure what to do"

    return message
# ------------------------------------


@app.route('/webhook1', methods=['GET'])
def validate():
    if request.args.get('hub.mode', '') == 'subscribe' and request.args.get('hub.verify_token', '') == VERIFICATION_TOKEN:
        return request.args.get('hub.challenge', '')
    else:
        return 'Failed validation.'


@app.route('/webhook1', methods=['POST'])
def webhook():
    data = request.get_json()
    process_request(data)
    return "ok", 200


def process_request(data):
    # Check if value correponding to object key is "page"
    if data["object"] == "page":
        # loop on the list correponding to entry key
        pid = data["entry"][0]['id']
        for entry in data["entry"]:
            # loop on the list correponding to the messaging key
            for messaging_event in entry["messaging"]:
                # access the messege event:
                # (1) get sender and recipient IDs
                sender_id = messaging_event["sender"]["id"]
                recipient_id = messaging_event["recipient"]["id"]
                # (2) check messege type is simple messege type
                if messaging_event.get("message") and pid == recipient_id:
                    # there is text key
                    if "text" in messaging_event["message"]:
                        messaging_text = messaging_event["message"]["text"]
                    else:
                        messaging_text = "no text"
                    get_wit(sender_id, messaging_text)


def get_wit(sender_id, msg):
    client = Wit(Wit_ACCESS_TOKEN)
    resp = client.message(msg)
    #message = "none"
    
    if len(resp.get('intents')) > 0:
        intent = resp.get('intents')[0].get('name')
        entity = list(resp.get('entities').values())[0][0].get('body')
        message = mmodule.main_function(intent, entity)
    else:
        message = "I'm not sure what to do"
        
    reply(sender_id, message)
    

def reply(sender_id, response):
    bot.send_text_message(sender_id, response)

port = int(os.environ.get('PORT', 8443))

if __name__ == "__main__":
      app.run(port=8443)
