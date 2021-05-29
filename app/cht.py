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

global tbot
global bot_token 
bot_token = "1805801633:AAGf_VfOwnP6WP61EwYTSTDlMw4_pcnzLQs"
bot_user_name = "movizsbot"
URL = "https://movizbot-server.herokuapp.com/"


tbot = telegram.Bot(token=bot_token)


@app.route('/{}'.format(bot_token), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), tbot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        bot_welcome = """
       Welcome to MovizBot
       """
        # send the welcoming message
        tbot.sendMessage(chat_id=chat_id, text=bot_welcome,
                         reply_to_message_id=msg_id)

    else:
        try:
            # clear the message we got from any non alphabets
            # create the api link for the avatar based on http://avatars.adorable.io/
            rep = wittel(text)
            # reply with a photo to the name the user sent,
            # note that you can send photos by url and telegram will fetch it for you
            tbot.sendMessage(chat_id=chat_id, text=rep,
                             reply_to_message_id=msg_id)
        except Exception:
            # if things went wrong
            tbot.sendMessage(
                chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = tbot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=bot_token))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


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
        
    reply(sender_id, message)
    '''

def reply(sender_id, response):
    bot.send_text_message(sender_id, response)


if __name__ == "__main__":
    app.run()
