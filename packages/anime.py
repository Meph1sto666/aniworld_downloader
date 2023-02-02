import pickle
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
		self.RESPONSE = requests.get(url)
		self.RAW_DATA = xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)*?</(no)?script>","",Bs(self.RESPONSE.text,"lxml").__str__()))
		self.URL = url + "/"
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
		self.SEASON_DATA = self.getSeasonData()
		self.SEASONS = self.getSeasons()
		del self.RAW_DATA
		del self.RESPONSE

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
		ds = getContent(self.RAW_DATA,"main_anime_release_start")
		if ds.lower() in ["heute"]:
			ds = Dt.now().year
		return Dt(int(ds),1,1)
	def getReleaseEnd(self) -> Dt:
		de = getContent(self.RAW_DATA,"main_anime_release_end")
		if de.lower() in ["heute"]:
			de = Dt.now().year
		return Dt(int(de),1,1)
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
	
	def getSeasonData(self) -> int:
		return getContent(self.RAW_DATA,"main_seasons_all")
	def getSeasons(self) -> list[Season]:
		if self.RESPONSE != None:
			sl = []
			for s in self.SEASON_DATA:
				if getContent(s, "main_season_url") != None:
					sl.append(Season(os.getenv("AW_URL_HOME") + getContent(s, "main_season_url")))
			return sl
		else: # only for testing without internet
			return [
				Season(None, 1, json.load(open("./tests/dmp1.json", "r")))
			]
		
		
	def createCoverUrl(self) -> str:
		return os.getenv("AW_URL_HOME") + self.COVER
	def createBackgroundUrl(self) -> str:
		return os.getenv("AW_URL_HOME") + self.BACKGROUND_IMG
	
	def __json__(self) -> dict:
		return {
			"id": self.ID,
			"jp_title": self.JP_TITLE,
			"en_title": self.DE_TITLE,
			"cover": self.createCoverUrl(),
			"background": self.createBackgroundUrl(),
			"release_start": self.RELEASE_START.isoformat(),
			"release_end": self.RELEASE_END.isoformat(),
			"fsk": self.FSK,
			"cast": [g.__json__() for g in self.CAST],
			"genres": {
				"main_genre": self.MAIN_GENRE.__json__(),
				"sub_genre": [g.__json__() for g in self.GENRES]
			},
			"seasons": [s.__json__() for s in self.SEASONS]
		}
	
	def __str__(self) -> str:
		return json.dumps(self.__json__())
	def save(self) -> None:
		path = f"./data/saves/"
		os.makedirs(path) if not os.path.exists(path) else None;
		pickle.dump(self,open(path + f"{self.ID}.awds","wb"),pickle.HIGHEST_PROTOCOL)
		
def animeFromJson(json) -> Anime:
	return Anime(None, json);

def load(id:int) -> Anime:
	path = f"./data/saves/{id}.awds"
	return pickle.load(open(path,"rb")) if os.path.exists(path) else None