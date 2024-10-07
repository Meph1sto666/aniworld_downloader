import typing
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By

class Stream:
	def __init__(self, redirect_url: str, language: int, season: int, episode: int) -> None:
		# self.host: typing.Literal["voe", "doodstream", "vidoza", "streamtape"] = host
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

	def download(self) -> str | None:
		raise NotImplementedError()
	
	def __to_json__(self) -> dict[str, typing.Any]:
		raise NotImplementedError()

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
		self.video_url = driver.find_element(By.ID, "mainvideo").get_attribute("src") #type: ignore
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