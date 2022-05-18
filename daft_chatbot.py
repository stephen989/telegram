import logging
import time
from telegram import Update, ForceReply, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
# import rte
# import reddit_download
import gym
# import schedule
import json
import os
# import accu
#quiet-springs-64791
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.info("Imports done")

def json_load(filename):
    if os.path.exists(filename):
        return json.load(open(filename, "r"))
    else:
        raise ValueError(f"{filename} does not exist")


def daft(update: Update, context: CallbackContext):
    print("choose daft")
    """Starts the conversation and displays headlines, asking user to choose one or exit."""
    person_id = update.effective_chat.id
    # headlines = rte.get_headlines()
    # text = "\n".join(headlines[:10])
    text = "Choose a thing to do. Or don't. Don't reallly care tbh."
    # reply_keyboard = [[1,2,3,4,5,6,7,8,9,10, "/x"]]
    reply_keyboard = [["Join list", "Leave list"], ["Create list", "/x"]]

    update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard
            , one_time_keyboard=True, 
            input_field_placeholder='Choose an option ffs.',
            resize_keyboard = True
        ),
    )

    return CHOOSE_DAFT

def choose_list(update: Update, context: CallbackContext):
    print("choose list")
    subscriptions = json_load("daft/subscriptions.txt")
    text = "Choose a list to join. Or don't. Don't reallly care tbh."
    # reply_keyboard = [[1,2,3,4,5,6,7,8,9,10, "/x"]]
    reply_keyboard = [list(subscriptions.keys())]

    update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True, 
            input_field_placeholder='Choose an option ffs.',
            resize_keyboard = True
        ),
    )

    return CHOOSE_LIST

def choose_remove_list(update: Update, context: CallbackContext):
    print("choose remove list")
    subscriptions = json_load("daft/subscriptions.txt")
    text = "Choose a list to leave. Or don't."
    # reply_keyboard = [[1,2,3,4,5,6,7,8,9,10, "/x"]]
    reply_keyboard = [list(subscriptions.keys())]

    update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True, 
            input_field_placeholder='Choose an option ffs.',
            resize_keyboard = True
        ),
    )

    return CHOOSE_REMOVE_LIST

def add_list(update: Update, context: CallbackContext):
    print("add list")
    subscriptions = json_load("daft/subscriptions.txt")

    user_id = update.effective_chat.id
    list_name = update.message.text
    subscriptions[list_name].append(user_id)
    json.dump(subscriptions, open("daft/subscriptions.txt", "w"))
    print(subscriptions)
    msg = "Thing completed."
    reply_keyboard = [["Menu", "/x"]]
    update.message.reply_text(
        msg,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='So...',
            resize_keyboard = True
        ),
    )
    print("done.")
    return ASK_EXIT

def remove_list(update: Update, context: CallbackContext):
    subscriptions = json_load("daft/subscriptions.txt")
    user_id = update.effective_chat.id
    list_name = update.message.text
    if user_id in subscriptions[list_name]:
        subscriptions[list_name].remove(user_id)
        json.dump(subscriptions, open("daft/subscriptions.txt", "w"))
    else:
        bot.send_message(user_id, "You're not on that list.")
    print(subscriptions)
    msg = "Thing completed."
    reply_keyboard = [["Menu", "/x"]]
    update.message.reply_text(
        msg,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='So...',
            resize_keyboard = True
        ),
    )
    return ASK_EXIT

def create_list(update: Update, context: CallbackContext):
    print("create list")
    subscriptions = json_load("daft/subscriptions.txt")
    daft_links = json_load("daft/daft_links.txt")
    daft_searches = json_load("daft/daft_searches.txt")
    user_id = update.effective_chat.id
    text = update.message.text.split(" ")
    url = text[-1]
    if (len(text) != 2) or ("https://www.daft.ie/property-for-rent" not in url):
        print(text)
        bot.send_message(user_id, "Incorrectly formatted. Contact Stephen for help")
    else:
        name, url = text
        subscriptions[name] = []
        daft_searches[name] = url
        daft_links[name] = dict()

        json.dump(subscriptions, open("daft/subscriptions.txt", "w"))
        json.dump(daft_links, open("daft/daft_links.txt", "w"))
        json.dump(daft_searches, open("daft/daft_searches.txt", "w"))
        bot.send_message(user_id, "Successfully created new list. Woo")

    print(subscriptions, daft_links.keys(), daft_searches)

    msg = "Thing completed."
    reply_keyboard = [["Menu", "/x"]]
    update.message.reply_text(
        msg,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='So...',
            resize_keyboard = True
        ),
    )
    return ASK_EXIT

def choose_create_list(update: Update, context: CallbackContext):
    print("choose create list")
    subscriptions = json_load("daft/subscriptions.txt")
    text = "Enter name and link to search seperated by space. E.g. d6_2bed https://daft.ie/..."
    reply_keyboard = [[1,2,3,4,5,6,7,8,9,10, "/x"]]
    # reply_keyboard = [list(subscriptions.keys())]

    update.message.reply_text(
        text
    )
    return CHOOSE_CREATE_LIST


with open("auth/telegram.txt") as f:
    main_token, other_token, my_id, sarah_id = f.read().splitlines()
current_token = main_token
bot = Bot(current_token)

def start(update: Update, context: CallbackContext):
    """Initial state where user chooses what function to use"""
    reply_keyboard = [["daft"], ["news"], ["gym"], ["weather"], ["animals"]]
    update.message.reply_text(
        "Hello",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose a story',
            resize_keyboard = True
        ),
    )

    return STATE

def get_weather(update: Update, context: CallbackContext):
    msg = gym.accuweather()
    reply_keyboard = [["Menu", "/x"]]

    update.message.reply_text(
        msg,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='So...',
            resize_keyboard = True
        ),
    )

    return ANIMAL


def ask_exit(update: Update, context: CallbackContext):
    reply_keyboard = [["Menu", "/x"]]
    update.message.reply_text("So...", reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='',
            resize_keyboard = True
        ),)
    return ASK_EXIT


def cancel(update: Update, context: CallbackContext):
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text("Peace.", reply_markup=ReplyKeyboardMarkup(
            [["/start"]], one_time_keyboard=True, input_field_placeholder='Click to restart',
            resize_keyboard = True
        ),)
    return ConversationHandler.END

def sorry(update: Update, context: CallbackContext):
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'We here at Stephen enterprises care deeply about your experience. However, the functionality you have chosen does not currently do anything so please stop choosing it.', reply_markup=ReplyKeyboardRemove()
    )
#     updater.stop()
    quit = cancel(update, context)
    return ConversationHandler.END


ANIMAL = 69
STATE, STORY, CONT, ASK_EXIT, BIO, ADD_LIST, CHOOSE_DAFT, REMOVE_LIST, CREATE_LIST, CHOOSE_LIST, CHOOSE_REMOVE_LIST, CHOOSE_CREATE_LIST = range(12)


choose_daft_options = [MessageHandler(Filters.regex(r"Join list"), choose_list), CommandHandler('x', cancel),
                          MessageHandler(Filters.regex(r"Create list"), choose_create_list), CommandHandler('x', cancel),
                          MessageHandler(Filters.regex(r"Leave list"), choose_remove_list), CommandHandler('x', cancel),
                          MessageHandler(Filters.regex(r"[0-9]"), add_list), CommandHandler('x', cancel)]



def main():
    
    updater = Updater(current_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # daft_handle = ConversationHandler(entry_points = [CommandHandler("start", start)])

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    # sarah_handler = ConversationHandler(
    #     entry_points=[CommandHandler('sarah', sarah)],
    #     states={
    #         STORY: [MessageHandler(Filters.regex("Yes, gimme animals"), sarah_howmany),
    #                 CommandHandler("otherfunctions", sorry),
    #                  CommandHandler("steeeeeeeeevee", sorry)],
    #
    #         ANIMAL: [MessageHandler(Filters.regex(r"[0-9]"), sarah_videos)],
    #
    #     },
    #     fallbacks=[CommandHandler('cancel', cancel)],
    # )
    main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STATE: [MessageHandler(Filters.regex("daft"), daft),
                    # MessageHandler(Filters.regex("animals"), sarah_howmany),
                    # MessageHandler(Filters.regex("gym"), get_gym),
                    CommandHandler('x', cancel)],
            CHOOSE_LIST: [MessageHandler(Filters.text & ~Filters.command, add_list)],
            CHOOSE_REMOVE_LIST: [MessageHandler(Filters.text & ~Filters.command, remove_list)],
            CHOOSE_CREATE_LIST: [MessageHandler(Filters.text & ~Filters.command, create_list)],
            CREATE_LIST: [MessageHandler(Filters.text & ~Filters.command, create_list)],
            CHOOSE_DAFT: choose_daft_options,
            CONT: [MessageHandler(Filters.regex(r"Yes"), news), CommandHandler('x', cancel)],
            ANIMAL: [MessageHandler(Filters.regex(r"[0-9]"), sarah_videos)],
            ASK_EXIT: [MessageHandler(Filters.regex(r"Menu"), start), CommandHandler('x', cancel)]
            
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(sarah_handler)
    dispatcher.add_handler(main_conv_handler)

    # Start the Bot
    updater.start_polling()
    while True:

        time.sleep(30)

if __name__ == "__main__":
    main()