import logging
import time
from telegram import Update, ForceReply, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
import os
import json
import requests
from bs4 import BeautifulSoup

# ssh -i daftykey.pem ec2-user@ec2-44-202-195-114.compute-1.amazonaws.com
# scp -i daftykey.pem -r final_chatbot  ec2-user@ec2-44-202-195-114.compute-1.amazonaws.com:

with open("auth/telegram.txt") as f:
    main_token, other_token, my_id, sarah_id = f.read().splitlines()
current_token = main_token
bot = Bot(current_token)
# Enable logging


def json_load(filename):
    if os.path.exists(filename):
        return json.load(open(filename, "r"))
    else:
        raise ValueError(f"{filename} does not exist")




def send_messages(search_name, messages):
    subscriptions = json_load("subscriptions.txt")
    members = subscriptions[search_name]
    for member in members:
        for message in messages:
            bot.send_message(member, message)

def test_search(search_name):
    print(search_name)
    daft_searches = json_load("daft_searches.txt")
    url = daft_searches[search_name]
    new_links = daft(url, search_name)
    if new_links:
        messages = [("https://daft.ie" + link + "\n" + details) for (link, details) in new_links]
        send_messages(search_name, messages)


    return new_links

def daft_loop():
    daft_searches = json_load("daft_searches.txt")
    for search_name in daft_searches.keys():
        print(search_name)
        url = daft_searches[search_name]
        new_links = daft(url, search_name)
        if new_links:
            messages = [("https://daft.ie"+link + "\n" + details) for (link , details) in new_links]
            send_messages(search_name, messages)
    return new_links


def daft(url, search_name):
    daft_links = json_load("daft_links.json")
    new_links = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    # get links and remove None values
    all_links = [link.get("href") for link in soup.find_all('a') if link.get("href")]
    # get relevant links
    # get relevant linksdaft_links.json
    links = [link for link in all_links  if "/for-rent" in link]
    for link in links:
        listing_id = link.split("/")[-1]
        if not daft_links[search_name].get(link):
            daft_links[search_name][link] = get_daft_details(link)
            new_links.append((link, get_daft_details(link)))
            print("new: ", search_name, link)
    json.dump(daft_links, open("daft_links.json", "w"))
    return new_links

def get_daft_details(link):
    url = "https://daft.ie" + link
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    price_block = soup.find(class_ = "TitleBlock__Price-sc-1avkvav-4 kPVHUm")
    if price_block:
        price = price_block.text + "\n"
    else:
        price = "Multiple prices\n"
    # if info_sections:
    info_sections = iter(soup.find_all(class_ = "PropertyPage__InfoSection-sc-14jmnho-7 dagRlp"))
    info = next(info_sections)
    try:
        while "Bedroom" not in info.text:
            info = next(info_sections)
    except Exception as e:
        info = False
    if not info:
        return " "
    text = price + "\n".join([child.text for child in info.children])
    return text


if __name__ == "__main__":
    while True:
        test_search("d4_2bed")
        # daft_loop()
        time.sleep(5)
