import xmltodict
from bs4 import BeautifulSoup as Bs
from datetime import datetime as Dt
import json
import os
import re
from packages.data_analyser import getContent
import requests
from packages.episode import Episode

class Season:
	def __init__(self, seasonUrl:str) -> None:
		if seasonUrl == None: return;
		# self.SEASON_NUM = seasonNum
		self.URL = seasonUrl + "/"
		self.RESPONSE = requests.get(self.URL)
		self.RAW_DATA = xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)*?</(no)?script>","",Bs(self.RESPONSE.text,"lxml").__str__()))
		self.TYPE = None;
		if "film" in self.URL.lower():
			self.TYPE = "other"
		elif "season" in self.URL.lower():
			self.TYPE = "season"
		self.EPISODES_DATA = getContent(self.RAW_DATA,"season_episodes_all")
		self.EPISODES = self.getEpisodes()
		del self.RESPONSE
		del self.RAW_DATA
		
	def getEpisodes(self) -> list[Episode]:
		el = []
		for e in self.EPISODES_DATA:
			if getContent(e, "season_episode_url") != None:
				el.append(Episode(os.getenv("AW_URL_HOME") + getContent(e, "season_episode_url")))
		return el

	def __json__(self) -> dict:
		return {
			"url": self.URL,
			"type": self.TYPE,
			"episodes": [e.__json__() for e in self.EPISODES]
		}

	def __str__(self) -> str:
		return json.dumps(self.__json__())