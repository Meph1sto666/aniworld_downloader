import os
import re
from time import sleep
import typing
import requests
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
import tqdm
from packages.errors import *

class Stream:
	def __init__(self, redirect_url: str, language: int, season: int, episode: int) -> None:
		self.redirect_url: str = redirect_url
		self.language: int = language
		self.video_url: str | None = None
		self.season: int = season
		self.episode: int = episode

	def __str__(self) -> str:
		return f"{self.language} / {self.redirect_url}"

	def open_selenium_session(self) -> WebDriver:
		driver: webdriver.Firefox = webdriver.Firefox()
		return driver

	def get_video_url(self, driver: WebDriver | None = None) -> str | None:
		raise NotImplementedError()
	
	def __to_json__(self) -> dict[str, typing.Any]:
		raise NotImplementedError()

	def download(self, filename: str) -> None:
		if not self.video_url:
			raise InvalidStreamURL()
		pbar = tqdm.tqdm(unit="B", desc=f"Downloading [S{str(self.season).rjust(2, '0')}E{str(self.episode).rjust(2, '0')}] from {self.__class__.__name__}", ascii=".#", unit_scale=True, leave=False)
		if os.path.exists(filename):
			pbar.write(f"Already downloaded {filename}")
			return
		pbar.write(f"Downloading {self.video_url} to {filename}")
		with open(filename, 'wb') as f:
			with requests.get(self.video_url, stream=True) as video_stream:
				pbar.total = int(video_stream.headers['Content-Length'])
				for chunk in video_stream.iter_content(1024):
					f.write(chunk)
					pbar.update(len(chunk))

class VOE(Stream):
	def __init__(self, redirect_url: str, language: int, season: int, episode: int) -> None:
		super().__init__(redirect_url, language, season, episode)
	def __to_json__(self) -> dict[str, typing.Any]:
		return {
            "redirect_url": self.redirect_url,
			"language": self.language,
			"video_url": self.video_url,
			"season": self.season,
            "episode": self.episode,
			"host": self.__class__.__name__
		}

class Vidoza(Stream):
	def __init__(self, redirect_url: str, language: int, season: int, episode: int) -> None:
		super().__init__(redirect_url, language, season, episode)

	def get_video_url(self, driver: WebDriver | None = None) -> str | None:
		if self.video_url: return self.video_url
		if not driver:
			driver = self.open_selenium_session()
		driver.get(self.redirect_url)
		self.video_url = driver.find_element(By.ID, "player_html5_api").get_attribute("src") #type: ignore
		return self.video_url

	def __to_json__(self) -> dict[str, typing.Any]:
		return {
            "redirect_url": self.redirect_url,
			"language": self.language,
			"video_url": self.video_url,
			"season": self.season,
            "episode": self.episode,
			"host": self.__class__.__name__
		}

class Doodstream(Stream):
	def __init__(self, redirect_url: str, language: int, season: int, episode: int) -> None:
		super().__init__(redirect_url, language, season, episode)

	def __to_json__(self) -> dict[str, typing.Any]:
		return {
            "redirect_url": self.redirect_url,
			"language": self.language,
			"video_url": self.video_url,
			"season": self.season,
            "episode": self.episode,
			"host": self.__class__.__name__
		}
	
class Streamtape(Stream):
	def __init__(self, redirect_url: str, language: int, season: int, episode: int) -> None:
		super().__init__(redirect_url, language, season, episode)

	def get_video_url(self, driver: WebDriver | None = None) -> str | None:
		if self.video_url: return self.video_url
		if not driver:
			driver = self.open_selenium_session()
		driver.get(self.redirect_url)
		# self.video_url = driver.find_element(By.ID, "mainvideo").get_attribute("src") #type: ignore
		self.video_url = "https:"+re.sub(r"&amp;", "&", re.search(r"(?<=>)\/\/streamtape.com/get_video.+(?=<)", driver.page_source).group())
		return self.video_url

	def __to_json__(self) -> dict[str, typing.Any]:
		return {
            "redirect_url": self.redirect_url,
			"language": self.language,
			"video_url": self.video_url,
			"season": self.season,
            "episode": self.episode,
			"host": self.__class__.__name__
		}