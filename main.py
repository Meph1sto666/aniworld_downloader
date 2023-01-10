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

a = anime.Anime("https://aniworld.to/anime/stream/arifureta-from-commonplace-to-worlds-strongest")
json.dump(xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)+?</(no)?script>","",BeautifulSoup(requests.get(url).text,"lxml").__str__())),open("./tests/anime.json","w"),indent=4)