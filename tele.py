import logging
import time
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import rte

token = "1821797506:AAEkBSG94JsIvEIgcsxrMDllXXxIWYXJ1tU"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Whale, hello there")


def deez_nuts(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Deez Nutz")
    time.sleep(3)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Goteem.")


def news(update: Update, context: CallbackContext) -> None:
    """Fetch news from rte and reply with text"""
    limit = 800
    if update.message.text.lower() == "news":
        headlines = rte.get_headlines()
        for k in range(0, int(1 + (len(headlines)-0.1)//15)):
            text = "\n".join(headlines[k*15:(k+1)*15])
            print(text)
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            time.sleep(3)
    elif update.message.text.isnumeric():
        i =  int(update.message.text)
        article_body = rte.get_full_article(i-1)
        # split article if length too long for one message
        pars = split_text(article_body)
        for par in pars:
            context.bot.send_message(chat_id=update.effective_chat.id, text=par)
            time.sleep(1)

        # for k in range(0, 1 + len(article_body)//limit):
        #     context.bot.send_message(chat_id=update.effective_chat.id, text=article_body[limit*k:limit*(k+1)])
        #     time.sleep(1.5)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "L")

def split_text(text, article = True):
    pars = text.split("\n")
    new_text = []
    while len(pars) > 0:
        new_par = ""
        while len(new_par) < 800 and len(pars)>0:
            new_par += pars[0]+"\n"
            pars.remove(pars[0])
        new_text.append(new_par)
    new_text[0] += 2*"\n"
    return new_text

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
dn_handler = CommandHandler("dn", deez_nuts)
dispatcher.add_handler(dn_handler)
news_handler = MessageHandler(Filters.text & (~Filters.command), news)
dispatcher.add_handler(news_handler)

updater.start_polling()
time.sleep(20)
updater.stop()

