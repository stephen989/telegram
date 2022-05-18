import logging
import time
from telegram import Update, ForceReply, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
import os
import json
import requests
from bs4 import BeautifulSoup

with open("auth/telegram.txt") as f:
    main_token, other_token, my_id, sarah_id = f.read().splitlines()
current_token = main_token
bot = Bot(current_token)
# Enable logging

reset_msg = "Bot resetting. Expect a lot of messages. :("

def json_load(filename):
    if os.path.exists(filename):
        return json.load(open(filename, "r"))
    else:
        raise ValueError(f"{filename} does not exist")


def reset():
	subscriptions = json_load("subscriptions.txt")
	all_subscribers = []
	for key in subscriptions.keys():
		all_subscribers += list(subscriptions[key])
	all_subscribers = list(set(all_subscribers))
	for sub in all_subscribers:
		bot.send_message(sub, reset_msg)

	daft_links = json_load("daft_links.txt")
	for link in daft_links.keys():
		daft_links[link] = dict()
	json.dump(daft_links, open("daft_links.txt", "w"))
	return None


if __name__ == "__main__":
	reset()




