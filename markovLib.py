import re
import spacy
import re
import markovify
import warnings
import requests
import re
from bs4 import BeautifulSoup

from nltk.corpus import gutenberg
warnings.filterwarnings("ignore")

nlp = spacy.load("en_core_web_sm")

def get_URLs():
    URL = "https://genius.com/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    chart = soup.find(id="top-songs")
    topSongs = chart.find_all("a", href=True)
    songURLs = []

    for element in topSongs:
        songURLs.append(element["href"])

    return songURLs


def get_raw_lyrics(urls):
    rawLyrics = ""
    for url in urls:
        lyricPage = requests.get(url)

        lyricSoup = BeautifulSoup(lyricPage.content, "html.parser")
        result = lyricSoup.find_all("div", {'data-lyrics-container': 'true'})

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


def generateText(sents, state_size=3, sentLength=""):
    if sentLength == "short":
        print(markovify.Text(sents, state_size).make_short_sentence(max_chars=40))

    print(markovify.Text(sents, state_size).make_sentence())


# get book texts and clean/format
walt = gutenberg.raw("whitman-leaves.txt")
blake = gutenberg.raw("blake-poems.txt")

walt_doc = nlp(walt)
blake_doc = nlp(blake)
walt_sents = ' '.join(
    [sent.text for sent in walt_doc.sents if len(sent.text) > 1])
blake_sents = ' '.join(
    [sent.text for sent in blake_doc.sents if len(sent.text) > 1])

walt = re.sub(r'Chapter \d+', '', text_cleaner(walt))
blake = re.sub(r'Chapter \d+', '', text_cleaner(blake))
walt = text_cleaner(walt)
blake = text_cleaner(blake)
cleanedText = walt_sents + blake_sents

# get song lyrics and clean/format
URLs = get_URLs()
rawLyrics = get_raw_lyrics(URLs)
cleanedLyrics = text_cleaner(rawLyrics)


for i in range(3):
    generateText(cleanedLyrics, state_size=2, sentLength="short")
