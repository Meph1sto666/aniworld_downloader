import xmltodict
from bs4 import BeautifulSoup as Bs
from datetime import datetime as Dt
import json
import os
import re
from packages.data_analyser import getContent as getContent
import requests
from packages.season import Season
from packages.genre import Genre
from packages.cast import Cast

class Anime:
    def __init__(self, url:str, rawData:dict=None) -> None:
        if url == None and rawData == None: return
        if url != None:
            self.RESPONSE = requests.get(url)
            self.RAW_DATA = xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)+?</(no)?script>","",Bs(self.RESPONSE.text,"lxml").__str__()))
            self.URL = url
        else:
            self.RAW_DATA = rawData
            self.URL = getContent(self.RAW_DATA,"main_url") +"/"
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
        self.CAST = self.getCast()
        self.SEASON_COUNT = self.getSeasonCount()
        self.SEASONS = self.getSeasons()

    def getTitleData(self) -> dict:
        return dict(getContent(self.RAW_DATA,"main_anime_title_data"))
    def getTitleDe(self) -> str:
        return getContent(self.RAW_DATA,"main_anime_title_de")
    def getTitleJp(self) -> str:
        return getContent(self.RAW_DATA,"main_anime_title_jp")
    def getCoverUrl(self) -> str:
        return getContent(self.RAW_DATA,"main_anime_cover")
    def getBackgroundUrl(self) -> str:
        return re.search(r"(?<=background-image: url\()(.+?)(?=\))",getContent(self.RAW_DATA,"main_anime_background_img")).group()
    def getReleaseStart(self) -> Dt:
        return Dt(int(getContent(self.RAW_DATA,"main_anime_release_start")),1,1)
    def getReleaseEnd(self) -> Dt:
        return Dt(int(getContent(self.RAW_DATA,"main_anime_release_end")),1,1)
    def getFsk(self) -> int:
        return int(getContent(self.RAW_DATA,"main_anime_fsk"))
    def getId(self) -> int:
        return int(getContent(self.RAW_DATA,"main_anime_id"))
    def getTrailerData(self) -> str:
        return getContent(self.RAW_DATA,"main_anime_trailer")

    def getGenreData(self) -> dict:
        return getContent(self.RAW_DATA,"main_genre_all")
    def getGenres(self) -> list[Genre]:
        gl = []
        [gl.append(Genre(getContent(i,"main_genre_name"))) if getContent(i,"main_genre_name") != None else None for i in self.getGenreData()]
        return gl
    def getMainGenre(self) -> Genre:
        return Genre(getContent(self.RAW_DATA,"main_genre_main"))
        
    def getCastData(self) -> dict:
        return getContent(self.RAW_DATA,"main_cast")
    def getCast(self) -> list[Cast]:
        cl = []
        for j in self.getCastData():
            j:dict
            n = getContent(j, "main_cast_all")
            if n == None: continue
            if type(n) == list:
                for p in n:
                    pt = getContent(p, "main_cast_item_name"), getContent(p, "main_cast_item_type")
                    if all([i != None for i in pt]):
                        cl.append(Cast(*pt))
            else:
                ptAlt = getContent(n, "main_cast_item_name"), getContent(n, "main_cast_item_type_alt")
                if all([i != None for i in ptAlt]):
                    cl.append(Cast(*ptAlt))
        return cl
    
    def getSeasonCount(self) -> int:
        return int(getContent(self.RAW_DATA,"main_season_count"))
    def getSeasons(self) -> list[Season]:
        return [Season(self.URL, s) for s in range(self.SEASON_COUNT)]
        
        
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
            "cast": [g.__str__() for g in self.CAST],
            "season_count": self.SEASON_COUNT,
            "seasons": [s.__str__() for s in self.SEASONS],
            "genres": {
                "main_genre": self.MAIN_GENRE.__str__(),
                "sub_genre": [g.__str__() for g in self.GENRES]
            }
        })
        
def animeFromJson(json) -> Anime:
    return Anime(None, json);