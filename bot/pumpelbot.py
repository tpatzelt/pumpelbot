#%%
import os
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater
import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
import click

@click.command()
@click.argument("telegram_token")
def main(telegram_token: str):
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    #%%
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         level=logging.INFO)
    #%%
    help_msg = "Bro, ich bin Pumpelbot. Schreib /free um zu erfahren" \
               " wieviele Freie Plätze es gerade im SuperFit Europacenter gibt."

    def help(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=help_msg)
    #%%
    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)
    #%%
    def free(update: Update, context: CallbackContext):
        url = "https://member.superfit.club/CheckinCounter/GetClubsCheckinCounterPage"
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, "html.parser")
        mydivs = soup.find_all("div", {"class": "col-md-12"})
        text = mydivs[1].text.replace("\n", "")
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    #%%
    free_spots_handler = CommandHandler('free', free)
    dispatcher.add_handler(free_spots_handler)

    #%%
    updater.start_polling()

if __name__ == '__main__':
    main()
