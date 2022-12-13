# %%
import logging
import os
import time

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Updater

from dataclasses import dataclass


@dataclass
class Flat:
    id: int
    info: str
    url: str

    def __eq__(self, other):
        return self.id == other.id

def parse_div_to_flat(div):
    id = get_flat_id(div)
    info = get_flat_info(div)
    url = get_flat_url(div)
    return Flat(id=id, info=info, url=url)

def get_flat_url(div):
    tag = div.find("a", {"class": "org-but"})
    return ("www.inberlinwohnen.de" + tag.get("href")).replace(" ", "%20")

def get_flat_info(div):
    tag = div.find("div", {"class": "list_col span_wflist_data"})
    return tag.text.strip().replace("\n\n", "\n")

def get_flat_id(div):
    tag = div.find("div", {"class": "tb-merkdetails"})
    return int(tag.get("id")[3:])

def get_flats(num=10):
    url = "https://inberlinwohnen.de/wohnungsfinder/?JrY36147-LZ"
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, "html.parser")
    mydivs = soup.find_all("li", {"class": "tb-merkflat ipg"})
    return [parse_div_to_flat(div) for div in mydivs[:num]]


def main():
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    help_msg = "Hi, ich poste Wohnungen von www.inberlinwohnen.de"

    def help(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=help_msg)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    def free(update: Update, context: CallbackContext):
        url = "https://member.superfit.club/CheckinCounter/GetClubsCheckinCounterPage"
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, "html.parser")
        mydivs = soup.find_all("div", {"class": "col-md-12"})
        text = mydivs[1].text.replace("\n", "")
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    free_spots_handler = CommandHandler('free', free)
    dispatcher.add_handler(free_spots_handler)

    def start_posting(update: Update, context: CallbackContext):
        old_flat_ids = set()
        while True:
            flats = get_flats()
            for flat in flats:
                if flat.id not in old_flat_ids:
                    context.bot.send_message(
                        chat_id= update.effective_chat.id, text=flat.url + "\n" + flat.info)
                    old_flat_ids.add(flat.id)
            time.sleep(120)

    start_posting_handler = CommandHandler("start_posting", start_posting)
    dispatcher.add_handler(start_posting_handler)


    updater.start_polling()
    updater.idle()
