import requests
import re
from bs4 import BeautifulSoup

def get_URLs():
    URL = "https://genius.com/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    chart = soup.find(id="top-songs")
    topSongs = chart.find_all("a", href= True)
    songURLs = []

    for element in topSongs:
        songURLs.append(element["href"])

    return songURLs

def get_raw_lyrics(urls):
    rawLyrics = ""
    for url in urls:
        lyricPage = requests.get(url)

        lyricSoup = BeautifulSoup(lyricPage.content, "html.parser")
        result = lyricSoup.find_all("div", {'data-lyrics-container':'true'})

        for tag in result:
            rawLyrics += " " + tag.text + " "
    
    return rawLyrics


def text_cleaner(text):
    text = re.sub(r'--', ' ', text)
    text = re.sub('[\[].*?[\]]', '', text)
    text = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b', '', text)
    text = re.sub(r"(\w)([A-Z])", r"\1 \2", text)
    text = text.replace("(", " ")
    text = text.replace(")", " ")
    text = text.replace('"', " ")
    text = text.replace(',', " ")
    text = ' '.join(text.split())
    return text