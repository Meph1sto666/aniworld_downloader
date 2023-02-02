import os
import requests
from selenium import webdriver
import time
from bs4 import BeautifulSoup as Bs
import json
from packages.data_analyser import getContent
import xmltodict
import re

class Stream:
	def __init__(self, redirectId:int, host:str, language:str) -> None:
		self.HOST = host
		self.REDIRECT_ID = redirectId
		self.LANGUAGE = language
		self.REDIRECT_URL:str = os.getenv("AW_URL_REDIRECT_BASE") + self.REDIRECT_ID + "/"
		self.URL:str = None
		self.VIDEO_URL:str = None

	def getStreamUrl(self) -> str:
		try:
			browser = webdriver.Firefox()
		except:
			browser = webdriver.Chrome()
		browser.get(self.REDIRECT_URL)
		while (self.REDIRECT_ID in browser.current_url):
			time.sleep(1)
		url = browser.current_url
		browser.close()
		return url
	
	def getVideoUrl(self) -> str:
		if self.URL == None:
			self.URL = self.getStreamUrl();
		if self.VIDEO_URL == None:
			raw = xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)*?</(no)?script>","",Bs(requests.get(self.URL).text,"lxml").__str__()))
			self.VIDEO_URL = getContent(raw,f"stream_{self.HOST.lower()}_video_source")
			json.dump(raw,open(f"./tests/{self.REDIRECT_ID}.json","w"),indent=4)
			print(f"stream_{self.HOST.lower()}_video_source")
		return self.VIDEO_URL
		
	def __json__(self) -> dict:
		j = {
			"host": self.HOST,
			"redirect_id": self.REDIRECT_ID,
			"language": self.LANGUAGE,
			"redirect_url": self.REDIRECT_URL
		}
		j["url"] = self.URL if self.URL != None else None
		j["video_url"] = self.VIDEO_URL if self.VIDEO_URL != None else None
		return j
	def __str__(self) -> str:
		return json.dumps(self.__json__())