import xmltodict
from bs4 import BeautifulSoup as Bs
from datetime import datetime as Dt
import json
import os
import re
from packages.data_analyser import getContent as getContent
import requests
from stream import Stream


class Episode:
    def __init__(self, episodeNum:int) -> None:
        self.EPISODE_NUM = episodeNum
        self.STREAMS = self.getStreams()
        
    def getStreamData() -> dict:
        return getContent(rawData, "stream_data")
    def getStreams() -> list[Stream]:
        pass