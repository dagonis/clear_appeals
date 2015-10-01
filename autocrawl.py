import os
import sys
import time

import requests

from bs4 import BeautifulSoup, SoupStrainer


def grab_pages(year):
    print("Parsing {} - {}".format(year, time.ctime()))
    year_page_file = open(str(year).split(".")[0] + "/" + year, "wb")
    year_page_content = requests.get(top_page + year)
    year_page_file.write(year_page_content.content)
    year_page_file.close()
    year_soup = BeautifulSoup(year_page_content.content, 'html.parser')
    for yl in year_soup.find_all("a"):
        try:
            if yl.has_attr('href'):
                if "-" in yl['href'] and len(yl['href']) > 10:
                    t_file = open(str(year).split(".")[0] + "/" + str(yl['href']).split("/")[-1], "wb")
                    t_file_req = requests.get(top_page + str(yl['href']).split("/")[-1])
                    t_file.write(t_file_req.content)
                    t_file.close()
        except Exception as e:
            print(e)
            sys.exit()
    print("Finished {} - {}".format(year, time.ctime()))


top_page = "http://www.dod.mil/dodgc/doha/industrial/"
top_page_content = requests.get(top_page)
soup = BeautifulSoup(top_page_content.content, 'html.parser')

for link in soup.find_all("a"):
    print(link)
    if link.has_attr('href'):
        if link['href'][0].isdigit():
            if not os.path.exists(str(link['href']).split(".")[0]):
                os.makedirs(str(link['href']).split(".")[0])
            if not link['href'].split(".")[0].endswith("15") and not link['href'].split(".")[0].endswith("14") and not link['href'].split(".")[0].endswith("13") and not link['href'].split(".")[0].endswith("12") and not link['href'].split(".")[0].endswith("11") and not link['href'].split(".")[0].endswith("10") and not link['href'].split(".")[0].endswith("09") and not link['href'].split(".")[0].endswith("08") and not link['href'].split(".")[0].endswith("07"):
                grab_pages(link['href'])