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
import json
from queue import Queue
from threading import Thread
from flask import Flask, request
from telegram.ext import MessageHandler, Filters

from telegram import Update
from telegram.ext import Dispatcher
import logging
import sys
import os

file_handler = logging.FileHandler(filename='log.txt',encoding='utf-8')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,handlers=handlers)

logger = logging.getLogger(__name__)
TOKEN = "1805801633:AAGf_VfOwnP6WP61EwYTSTDlMw4_pcnzLQs"
NAME = "movizbot-server"




tbot = telegram.Bot(token=TOKEN)
def echo(update, context):
    text = update.message.text
    update.message.reply_text(wittel(text))

def setup(TOKEN):
    # update queue and dispatcher instances
    update_queue = Queue()

    dispatcher = Dispatcher(tbot, update_queue, use_context=True)

    ##### Register handlers here #####
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    # Start the thread
    tbot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()

    return update_queue
    # you might want to return dispatcher as well,
    # to stop it at server shutdown, or to register more handlers:
    # return (update_queue, dispatcher)

update_queue = setup(TOKEN)

@app.route('/' + TOKEN, methods=['GET','POST'])
def pass_update():
    new_update = Update.de_json(request.get_json(force=True),bot)
    update_queue.put(new_update)
    return "ok"

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
    message = "none"
    '''
    if len(resp.get('intents')) > 0:
        intent = resp.get('intents')[0].get('name')
        entity = list(resp.get('entities').values())[0][0].get('body')
        message = mmodule.main_function(intent, entity)
    else:
        message = "I'm not sure what to do"
    '''    
    reply(sender_id, message)
    

def reply(sender_id, response):
    bot.send_text_message(sender_id, response)

PORT = int(os.environ.get('PORT', '8443'))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=PORT,debug=True)
