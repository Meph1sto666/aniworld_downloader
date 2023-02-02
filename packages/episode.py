import typing
import xmltodict
from bs4 import BeautifulSoup as Bs
from datetime import datetime as Dt
import json
import os
import re
from packages.data_analyser import getContent as getContent
import requests
from packages.stream import Stream

DICTIONARY_FILE = "./data/dictioonary.json"

class Episode:
	def __init__(self, episodeUrl:str) -> None:
		if episodeUrl == None: return;
		self.URL = episodeUrl + "/"
		self.RESPONSE = requests.get(self.URL)
		self.RAW_DATA = xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)*?</(no)?script>","",Bs(self.RESPONSE.text,"lxml").__str__()))
		self.EPISODE_NUM = getContent(self.RAW_DATA,"episode_num")
		self.EPISODE_ID = int(getContent(self.RAW_DATA, "episode_id"))
		self.LANGUAGE_DATA = getContent(self.RAW_DATA,"episode_language_data")
		self.SEASON_ID = int(getContent(self.RAW_DATA, "episode_season_id"))
		self.TITLES = getContent(self.RAW_DATA, "episode_titles")
		self.DESCRIPTION = getContent(self.RAW_DATA, "episode_description")
		self.LANGUAGES = self.getLanguages()
		self.STREAMS = self.getStreams()
		del self.RESPONSE
		del self.RAW_DATA
		
	def getStreamData(self) -> dict:
		return getContent(self.RAW_DATA, "stream_data")
	def getStreams(self) -> list[Stream]:
		return [Stream(getContent(s,"stream_redirect_id"),getContent(s,"stream_host_name"),self.getStreamLanguageFromLanguageId(int(getContent(s,"stream_language_id")))) for s in getContent(self.RAW_DATA,"stream_data")]
	def getLanguages(self) -> dict:
		ldict = {}
		if type(self.LANGUAGE_DATA) == dict:
			ldict[getContent(self.LANGUAGE_DATA,"episode_language_id")] = self.streamLangTextToLang(getContent(self.LANGUAGE_DATA,"episode_language_name"))
		else:
			for l in self.LANGUAGE_DATA:
				ldict[getContent(l,"episode_language_id")] = self.streamLangTextToLang(getContent(l,"episode_language_name"))
		return ldict
	def getStreamLanguageFromLanguageId(self, id:int) -> str:
		return self.LANGUAGES.get(str(id))
			
	def streamLangTextToLang(self,langText:str) -> str: 
		if "deutsch" in langText.lower():
			lang = "ger"
		elif "englisch" in langText.lower():
			lang = "eng"
		if "unter" in langText.lower():
			lang += "-sub"
		return lang

	def download(self, host:str, language:str) -> None:
		streams = self.streamFilter(host, language)
		if len(streams) < 1:
			print("FAILED TO DOWNLOAD! NO STREAMS MATCHIN TAGS FOUND")
			return
		url = streams[0].getVideoUrl()
		with open("downloads/" + str(self.EPISODE_ID) + ".mp4", "wb") as f: #NOTE: FIIIIIIIIIX naming
			f:typing.TextIO
			with requests.get(url) as r:
				r:requests.Response
				for c in r.iter_content(1024):
					f.write(c)
		
	
	def __json__(self) -> dict:
		return {
			"url": self.URL,
			"episode_num": self.EPISODE_NUM,
			"episode_id": self.EPISODE_ID,
			"language": self.LANGUAGES,
			"SEASON_ID": self.SEASON_ID,
			"titles": self.TITLES,
			"description": self.DESCRIPTION,
			"streams": [s.__json__() for s in self.STREAMS]
		}
	
	def __str__(self) -> str:
		return json.dumps(self.__json__())

	def streamFilter(self, fHost:str=None, fLang:str=None, invert:bool=False) -> list[Stream]:
		streams = self.STREAMS;
		if fHost != None:
			streams = list(filter(lambda s: (s.HOST.lower() == fHost) != invert, streams));
		if fLang != None:
			streams = list(filter(lambda s: (s.LANGUAGE.lower() == fLang) != invert, streams));
		return streams