import xmltodict
from bs4 import BeautifulSoup as Bs
from datetime import datetime as Dt
import json
import os
import re
from packages.data_analyser import getContent as getContent
import requests
from packages.episode import Episode

class Season:
    def __init__(self, animeUrl:str, seasonNum:int, rawData:dict=None) -> None:
        if animeUrl == None and rawData == None: return;
        self.SEASON_NUM = seasonNum
        if animeUrl != None:
            self.URL = animeUrl + os.getenv("AW_URL_SEASON_KEY") + str(seasonNum)
            self.RESPONSE = requests.get(self.URL)
            self.RAW_DATA = xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)+?</(no)?script>","",Bs(self.RESPONSE.text,"lxml").__str__()))
        else:
            self.RAW_DATA = rawData
            self.URL = getContent("main_url") + "/"
        self.EPISODES = self.getEpisodes()
        
        
    def getEpisodes(self) -> list[Episode]:
        el = [];
        
        return el