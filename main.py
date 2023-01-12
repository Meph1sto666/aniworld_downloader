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
a = anime.animeFromJson(json.load(open("./tests/dmp0.json", "r")))

print(a)