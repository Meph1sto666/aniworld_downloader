import re
import requests
import json
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from packages import home
import xmltodict
from packages import anime
load_dotenv();
from packages import data_analyser


# a = anime.Anime("https://aniworld.to/anime/stream/horimiya")
a = anime.Anime("https://aniworld.to/anime/stream/danmachi-is-it-wrong-to-try-to-pick-up-girls-in-a-dungeon")
# a = anime.animeFromJson(json.load(open("./tests/dmp0.json", "r")))

# print(a.SEASONS[0].EPISODES[0].STREAMS[0].HOST)
# print(a.SEASONS[0].EPISODES[0].STREAMS[0].REDIRECT_ID)
# print(a.SEASONS[0].EPISODES[0].STREAMS[0].LANGUAGE)
print(a.SEASONS)