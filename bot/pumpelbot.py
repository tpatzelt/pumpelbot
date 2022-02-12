# %%
import logging
import os

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Updater

from bot.visualize import weekday_plot, mapping


def main():
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    # %%
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    # %%
    help_msg = "Bro, ich bin Pumpelbot. Schreib /free um zu erfahren" \
               " wieviele Freie Plätze es gerade im SuperFit Europacenter gibt."

    def help(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=help_msg)

    # %%
    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    # %%
    def free(update: Update, context: CallbackContext):
        url = "https://member.superfit.club/CheckinCounter/GetClubsCheckinCounterPage"
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, "html.parser")
        mydivs = soup.find_all("div", {"class": "col-md-12"})
        text = mydivs[1].text.replace("\n", "")
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    # %%
    free_spots_handler = CommandHandler('free', free)
    dispatcher.add_handler(free_spots_handler)

    def plot_factory(weekday: int):
        def func(update, context):
            return weekday_plot(weekday=weekday, update=update, context=context)

        return func

    for weekday in mapping:
        handler = CommandHandler(mapping[weekday], plot_factory(weekday=weekday))
        dispatcher.add_handler(handler)

    def list_weekdays(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="\\" + f"\n\\".join(list(mapping.values())))

    list_weekdays_handler = CommandHandler("weekdays", list_weekdays)
    dispatcher.add_handler(list_weekdays_handler)

    # %%
    updater.start_polling()


if __name__ == '__main__':
    main()
