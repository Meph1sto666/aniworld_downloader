import xmltodict
from bs4 import BeautifulSoup as Bs
from datetime import datetime as Dt
import json
import os
import re
from packages import data_analyser
import requests

class Genre:
    def __init__(self, name:str, mainGenre:bool=False) -> None:
        self.MAIN_GENRE = mainGenre
        self.NAME = name.lower()
    def __str__(self) -> str:
        j = {
            "name": self.NAME
        }
        if self.MAIN_GENRE:
            j["main_genre"] = self.MAIN_GENRE
        return json.dumps(j)

class Person:
    def __init__(self, name:str, job:str) -> None:
        self.NAME = name
        self.JOB = job
    def __str__(self) -> str:
        return json.dumps({
            "name": self.NAME,
            "job": self.JOB
        })

class Anime:
    def __init__(self, url:str) -> None:
        self.RESPONSE = requests.get(url)
        self.RAW_DATA = xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)+?</(no)?script>","",Bs(requests.get(url).text,"lxml").__str__()))
        self.title_data = self.getTitleData()
        self.JP_TITLE = self.getTitleJp()
        self.DE_TITLE = self.getTitleDe()
        self.COVER = self.getCoverUrl()
        self.BACKGROUND_IMG = self.getBackgroundUrl()
        self.RELEASE_START = self.getReleaseStart()
        self.RELEASE_END = self.getReleaseEnd()
        self.FSK = self.getFsk()
        self.ID = self.getId()

        self.GENRES = self.getGenres()
        self.MAIN_GENRE = self.getMainGenre()
        
    def getTitleData(self) -> dict:
        return dict(data_analyser.getContent(self.RAW_DATA,"main_anime_title_data"))
    def getTitleDe(self) -> str:
        return data_analyser.getContent(self.RAW_DATA,"main_anime_title_de")
    def getTitleJp(self) -> str:
        return data_analyser.getContent(self.RAW_DATA,"main_anime_title_jp")
    def getCoverUrl(self) -> str:
        return data_analyser.getContent(self.RAW_DATA,"main_anime_cover")
    def getBackgroundUrl(self) -> str:
        return re.search(r"(?<=background-image: url\()(.+?)(?=\))",data_analyser.getContent(self.RAW_DATA,"main_anime_background_img")).group()
    def getReleaseStart(self) -> Dt:
        return Dt(int(data_analyser.getContent(self.RAW_DATA,"main_anime_release_start")),1,1)
    def getReleaseEnd(self) -> Dt:
        return Dt(int(data_analyser.getContent(self.RAW_DATA,"main_anime_release_end")),1,1)
    def getFsk(self) -> int:
        return int(data_analyser.getContent(self.RAW_DATA,"main_anime_fsk"))
    def getId(self) -> int:
        return int(data_analyser.getContent(self.RAW_DATA,"main_anime_id"))
    def getTrailerData(self) -> str:
        return data_analyser.getContent(self.RAW_DATA,"main_anime_trailer")
    def getGenreData(self) -> dict:
        return data_analyser.getContent(self.RAW_DATA,"main_genre_all")

    def getGenres(self) -> list[Genre]:
        gl = []
        [gl.append(Genre(data_analyser.getContent(i,"main_genre_name"))) if data_analyser.getContent(i,"main_genre_name") != None else None for i in self.getGenreData()]
        return gl
    def getMainGenre(self) -> Genre:
        return Genre(data_analyser.getContent(self.RAW_DATA,"main_genre_main"))
    
    
    def createCoverUrl(self) -> str:
        return os.getenv("AW_URL_HOME") + self.COVER
    def createBackgroundUrl(self) -> str:
        return os.getenv("AW_URL_HOME") + self.BACKGROUND_IMG
    
    def __str__(self) -> str:
        return json.dumps({
            "id": self.ID,
            "jp_title": self.JP_TITLE,
            "en_title": self.DE_TITLE,
            "cover": self.createCoverUrl(),
            "background": self.createBackgroundUrl(),
            "release_start": self.RELEASE_START.isoformat(),
            "release_end": self.RELEASE_END.isoformat(),
            "fsk": self.FSK,
            "genres": {
                "main_genre": self.MAIN_GENRE.__str__(),
                "sub_genre": [g.__str__() for g in self.GENRES]
            }
        })
class Season:
    def __init__(self, seasonNum:int) -> None:
        self.SEASON_NUM = seasonNum
        
class Episode:
    def __init__(self, episodeNum:int) -> None:
        self.EPISODE_NUM = episodeNum