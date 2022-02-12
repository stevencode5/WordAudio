import os
import requests
from bs4 import BeautifulSoup

WORDREFERENCE_HOSTNAME = "https://www.wordreference.com"
WORDREFERENCE_BASE_URL = "https://www.wordreference.com/es/translation.asp?tranword="
CAMBRIDGE_HOTSNAME = "https://dictionary.cambridge.org/"
CAMBRIDGE_BASE_URL = "https://dictionary.cambridge.org/dictionary/english/"


def process_audio_url(word_name):
    try:
        download_audio_url = calculate_audio_url(word_name)
        download_audio(download_audio_url, word_name)
        move_audio_to_download_directory(word_name)
    except Exception as e:
        print(e)


def calculate_audio_url(word_name):
    wordreference_url = calculate_wordreference_url(word_name)
    if wordreference_url:
        return wordreference_url

    cambridge_url = calculate_cambridge_url(word_name)
    if cambridge_url:
        return cambridge_url

    raise Exception("No word found")


def calculate_wordreference_url(word_name):
    main_url = WORDREFERENCE_BASE_URL + word_name
    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    audio_source = soup.find("source")
    if not audio_source:
        return ""
    audio_url = audio_source["src"]
    download_url = WORDREFERENCE_HOSTNAME + audio_url
    return download_url


def calculate_cambridge_url(word_name):
    main_url = CAMBRIDGE_BASE_URL + word_name
    page = requests.get(main_url, headers={"User-Agent": "Mozilla/5.0"})  # Cambridge its necessary to set the browser
    soup = BeautifulSoup(page.content, 'html.parser')
    audio_span = soup.find_all("span", {"class": "us dpron-i"})
    audio_url = audio_span[0].contents[1].contents[1].contents[3]["src"]
    if not audio_url:
        return ""
    return CAMBRIDGE_HOTSNAME + audio_url


def download_audio(download_url, audio_name):
    r = requests.get(download_url, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
    open(f"{audio_name}.mp3", 'wb').write(r.content)
    print(f"{audio_name}.mp3 Downloaded !")


def move_audio_to_download_directory(audio_name):
    os.rename(f"{audio_name}.mp3", f"/home/jaime/Downloads/{audio_name}.mp3")


while True:
    word = input()

    if word == "exit":
        break

    process_audio_url(word)
