import json
import os
import re
import time
from selenium import webdriver
from packages.anime import Anime
from packages.streams import Stream, Streamtape
from selenium.webdriver.common.by import By

# a = Anime("https://aniworld.to/anime/stream/arifureta-from-commonplace-to-worlds-strongest")
a = Anime("https://aniworld.to/anime/stream/arknights-prelude-to-dawn")

options = webdriver.FirefoxOptions()
options.add_argument("--headless") # type: ignore

driver = webdriver.Firefox(options=options)
for e in a.get_all_episodes():
	stream: Stream | None = e.get_best_download_stream(3)
	if not stream: continue
	print(stream.get_video_url(driver))

driver.close()

a.download(3)

os.makedirs("./saves/", exist_ok=True)
os.makedirs(f"./downloads/{a.work_title}", exist_ok=True)
json.dump(a.__to_json__(), open(f"./saves/{a.work_title}", "w"))
