import requests
from bs4 import BeautifulSoup

#show_id = input("Title/Show ID: ")

pagedata = requests.get(
    f"https://www.netflix.com/sa/title/8099213",
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
)

parsed_html = BeautifulSoup(pagedata.text, features='html.parser')
title = BeautifulSoup.select_one(parsed_html, ".title-title")

if not title:
    input("Show not found. press any key to exit...")
    exit()

title = title.text


