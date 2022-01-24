import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

newline = "\n"
# with open("free_spots_counts.csv", "w") as fp:
#     fp.write("free_spots, datetime"+newline)

pattern = re.compile("\d+")
url = "https://member.superfit.club/CheckinCounter/GetClubsCheckinCounterPage"
while True:
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, "html.parser")
    mydivs = soup.find_all("div", {"class": "col-md-12"})
    free_spots = pattern.findall(mydivs[2].text)[0]
    print(free_spots, datetime.now())
    with open("free_spots_counts.csv", "a") as fp:
        fp.write(free_spots + "," + str(datetime.now()) + newline)
    time.sleep(60*5)
