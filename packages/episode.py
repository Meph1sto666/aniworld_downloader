import xmltodict
from bs4 import BeautifulSoup as Bs
from datetime import datetime as Dt
import json
import os
import re
from packages.data_analyser import getContent as getContent
import requests
from packages.stream import Stream


class Episode:
    def __init__(self, seasonUrl:str, episodeNum:int, rawData:dict=None) -> None:
        if seasonUrl == None and rawData == None: return;
        self.EPISODE_NUM = episodeNum
        if seasonUrl != None:
            self.URL = seasonUrl + os.getenv("AW_URL_EPISODE_KEY") + str(episodeNum)
            self.RESPONSE = requests.get(self.URL)
            self.RAW_DATA = xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)+?</(no)?script>","",Bs(self.RESPONSE.text,"lxml").__str__()))
        else:
            self.RAW_DATA = rawData
            self.URL = getContent("main_url") + "/"
        
        self.EPISODE_NUM = episodeNum
        self.STREAMS = self.getStreams()
        
    def getStreamData(self) -> dict:
        return getContent(self.RAW_DATA, "stream_data")
    def getStreams() -> list[Stream]:
        pass