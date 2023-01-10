from bs4 import BeautifulSoup as Bs
import json
import os
import re

import requests

class Anime:
    def __init__(self, url:str) -> None:
        self.RESPONSE = requests.get(url)
        self.RAW_DATA = Bs(self.RESPONSE.text, "lxml")
        # self.NAME = name

    def getNameFromData(self) -> str:
        return self.RAW_DATA.select("a")
    
class Season:
    def __init__(self, seasonNum:int) -> None:
        self.SEASON_NUM = seasonNum
        
class Episode:
    def __init__(self, episodeNum:int) -> None:
        self.EPISODE_NUM = episodeNum