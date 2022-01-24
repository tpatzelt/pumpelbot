import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import CallbackContext
from pathlib import Path
import csv
from datetime import datetime, timedelta
import pandas as pd

mapping = dict(zip(range(7),["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]))

def weekday_plot(weekday: int, update: Update, context: CallbackContext):
    data = dict()
    with open("free_spots_counts.csv", "r") as fp:
        csv_reader = csv.DictReader(fp, delimiter=',')
        for row in csv_reader:
            dt = datetime.fromisoformat(row[" datetime"])
            delta = timedelta(hours=1)
            data[dt + delta] = row["free_spots"]
    path = Path("weekday-plot.jpg")
    data_df = pd.DataFrame(data=[(i, k) for i, k in data.items()])
    # %%
    data_df[1] = data_df[1].astype(int)
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