import os
import re
import time
from datetime import datetime

import pymongo
import requests
from bs4 import BeautifulSoup

db_password = os.environ.get("DB_PASSWORD")
client = pymongo.MongoClient(
    f"mongodb+srv://tpatzelt:{db_password}@pumpelbotdb.hmwgc.mongodb.net/PumpelBotDB?retryWrites=true&w=majority")
db = client.free_spots

pattern = re.compile("\d+")
url = "https://member.superfit.club/CheckinCounter/GetClubsCheckinCounterPage"
while True:
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, "html.parser")
    mydivs = soup.find_all("div", {"class": "col-md-12"})
    free_spots = pattern.findall(mydivs[2].text)[0]
    print(free_spots, datetime.now())
    post = {"free_spots": int(free_spots), "datetime": datetime.now()}
    db.posts.insert_one(post)
    time.sleep(60 * 5)
