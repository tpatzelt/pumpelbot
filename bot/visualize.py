import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pymongo
from telegram import Update
from telegram.ext import CallbackContext

mapping = dict(
    zip(range(7), ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]))


def weekday_plot(weekday: int, update: Update, context: CallbackContext):
    db_password = os.environ.get("DB_PASSWORD")
    client = pymongo.MongoClient(
        f"mongodb+srv://tpatzelt:{db_password}@pumpelbotdb.hmwgc.mongodb.net/PumpelBotDB?retryWrites=true&w=majority")
    db = client.free_spots
    data_df = pd.DataFrame(
        data=[(post["datetime"], post["free_spots"]) for post in db.posts.find()])
    data_df[1] = data_df[1].astype(int)
    path = Path("weekday-plot.jpg")
    g = None
    for group in data_df.groupby(data_df[0].dt.weekday):
        day, day_df = group
        if day != weekday:
            continue
        day_df.groupby(day_df[0].dt.hour).mean().apply(lambda x: 167 - x).plot.bar()
        plt.title(mapping[weekday])
        plt.xlabel("Uhrzeit")
        plt.ylabel("Besucher")
        plt.legend(["Pumpelbros"])
        break
    plt.savefig(path)
    with open(path, "rb") as fp:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=fp)
    path.unlink()
