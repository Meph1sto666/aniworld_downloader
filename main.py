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
from bs4 import BeautifulSoup as Bs

# a = anime.Anime("https://aniworld.to/anime/stream/arifureta-from-commonplace-to-worlds-strongest")
# a = anime.Anime("https://aniworld.to/anime/stream/danmachi-is-it-wrong-to-try-to-pick-up-girls-in-a-dungeon")
# a = anime.animeFromJson(json.load(open("./tests/dmp0.json", "r")))
# a = anime.Anime("https://aniworld.to/anime/stream/the-misfit-of-demon-king-academy")
url = "https://aniworld.to/redirect/1363879"

# json.dump(a.__json__(),open("./tests/serialized.json", "w"), indent = 4)

# for i in range(len(a.SEASONS[1].EPISODES[0].STREAMS)):
# 	print(a.SEASONS[1].EPISODES[0].STREAMS[i].REDIRECT_ID)


# response:requests.Response = requests.get(url)
# response:requests.Response = requests.head(url)

# print(response.headers.get("location"))
# print(response.url)

print(requests.get("https://vidoza.net/embed-9rq7sa23mq06.html"))

# json.dump(xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)+?</(no)?script>","",Bs(requests.get(requests.get(url).url).text,"lxml").__str__())), open("./tests/redirect_page.json", "w"),indent=4)