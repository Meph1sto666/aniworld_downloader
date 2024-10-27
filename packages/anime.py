import json
import os
import typing
from bs4 import BeautifulSoup as Bs
import re
import xmltodict
import requests
from packages.streams import Stream
import packages.streams as streams
from packages.errors import *
from concurrent import futures
import tqdm

class Season:
	def __init__(self, url: str) -> None:
		self.url: str = url
		self.RAW_DATA: xmltodict.OrderedDict[str, json.Any] = xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)+?</(no)?script>", "", Bs(requests.get(url).text, features="html.parser").__str__())) #type: ignore
		raw_episodes:list[dict[str, typing.Any]] = self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][2]["table"]["tbody"]["tr"] #type: ignore
		self.episodes: list[Episode] = []
		if not isinstance(raw_episodes, dict):
			for e in raw_episodes: #type: ignore
				ep_url: str = str("https://aniworld.to"+e["td"][0]["a"]["@href"]) #type: ignore
				self.episodes.append(Episode(ep_url))

	def __to_json__(self) -> dict[str, typing.Any]:
		return {
			"episodes": [e.__to_json__() for e in self.episodes],
            "url": self.url
		}

class Episode:
	def __init__(self, url: str) -> None:
		self.RAW_DATA: xmltodict.OrderedDict[str, json.Any] = xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)+?</(no)?script>", "", Bs(requests.get(url).text, features="html.parser").__str__())) #type: ignore
		self.url: str = url
		self.anime_work_title: str = re.search(r"(?<=stream\/)[^\/\s]+", url).group() # type: ignore
		self.title: str = self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][2]["div"][2]["h2"]["span"]["#text"] #type: ignore
		self.english_title: str = self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][2]["div"][2]["h2"]["small"]["#text"] #type: ignore
		self.episode_number: int = int(self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][2]["div"][2]["@data-episode"]) #type: ignore
		self.season_number: int = int(self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][2]["div"][2]["@data-season"]) #type: ignore
		self.streams: list[Stream] = [
			getattr(streams, s.get("div").get("a").get("h4"))( #type: ignore
				redirect_url="https://aniworld.to"+s.get("@data-link-target"), #type: ignore
				language=int(s.get("@data-lang-key")), #type: ignore
				season=self.season_number,
				episode=self.episode_number
			) for s in self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][2]["div"][4]["ul"]["li"] #type: ignore
		]
		self.STREAM_PRIORITY: dict[str, int] = {
			"vidoza": 0,
			"streamtape": 1,
			"doodstream": 2,
			"voe": 3
		}
	def __to_json__(self) -> dict[str, typing.Any]:
		return {
            "url": self.url,
			"title": self.title,
			"english_title": self.english_title,
			"episode_number": self.episode_number,
			"season_number": self.season_number,
			"streams": [s.__to_json__() for s in self.streams]
		}

	def get_stream(self, language: int, host: typing.Literal["voe", "doodstream", "vidoza", "streamtape"]) -> Stream | None:
		found: list[Stream] = sorted(list(filter(lambda x: x.language == language and host == x.__class__.__name__.lower(), self.streams)), key=lambda x: self.STREAM_PRIORITY.get(x.__class__.__name__.lower(), 5))
		return found[0] if found else None

	def get_best_download_stream(self, language: int) -> Stream:
		found: list[Stream] = sorted(list(filter(lambda x: (x.language == language) and (isinstance(x, (streams.Vidoza, streams.Streamtape))), self.streams)), key=lambda x: self.STREAM_PRIORITY.get(x.__class__.__name__.lower(), 5))
		if found:
			return found[0]
		else:
			raise StreamsDoNotSupportDownload()
	
	def download(self, language: int) -> None:
		s: Stream = self.get_best_download_stream(language)
		os.makedirs(f"./downloads/{self.anime_work_title}", exist_ok=True)
		s.download(f"./downloads/{self.anime_work_title}/{self.anime_work_title}_S{str(self.season_number).rjust(2, '0')}_E{str(self.episode_number).rjust(2, '0')}.mp4")

class Movie:
	def __init__(self, url: str) -> None:
		self.RAW_DATA: xmltodict.OrderedDict[str, json.Any] = xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)+?</(no)?script>", "", Bs(requests.get(url).text, features="html.parser").__str__())) #type: ignore
		return
		self.url: str = url
		self.anime_work_title: str = re.search(r"(?<=stream\/)[^\/\s]+", url).group() # type: ignore
		self.title: str = self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][2]["div"][2]["h2"]["span"]["#text"] #type: ignore
		self.english_title: str = self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][2]["div"][2]["h2"]["small"]["#text"] #type: ignore
		self.episode_number: int = int(self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][2]["div"][2]["@data-episode"]) #type: ignore
		self.season_number: int = int(self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][2]["div"][2]["@data-season"]) #type: ignore
		self.streams: list[Stream] = [
			getattr(streams, s.get("div").get("a").get("h4"))( #type: ignore
				redirect_url="https://aniworld.to"+s.get("@data-link-target"), #type: ignore
				language=int(s.get("@data-lang-key")), #type: ignore
				season=self.season_number,
				episode=self.episode_number
			) for s in self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][2]["div"][4]["ul"]["li"] #type: ignore
		]
		self.STREAM_PRIORITY: dict[str, int] = {
			"vidoza": 0,
			"streamtape": 1,
			"doodstream": 2,
			"voe": 3
		}
	def __to_json__(self) -> dict[str, typing.Any]:
		raise NotImplementedError()
		return {
            "url": self.url,
			"title": self.title,
			"english_title": self.english_title,
			"episode_number": self.episode_number,
			"season_number": self.season_number,
			"streams": [s.__to_json__() for s in self.streams]
		}

	def get_stream(self, language: int, host: typing.Literal["voe", "doodstream", "vidoza", "streamtape"]) -> Stream | None:
		raise NotImplementedError()

		found: list[Stream] = sorted(list(filter(lambda x: x.language == language and host == x.__class__.__name__.lower(), self.streams)), key=lambda x: self.STREAM_PRIORITY.get(x.__class__.__name__.lower(), 5))
		return found[0] if found else None

	def get_best_download_stream(self, language: int) -> Stream:
		raise NotImplementedError()

		found: list[Stream] = sorted(list(filter(lambda x: (x.language == language) and (isinstance(x, (streams.Vidoza, streams.Streamtape))), self.streams)), key=lambda x: self.STREAM_PRIORITY.get(x.__class__.__name__.lower(), 5))
		if found:
			return found[0]
		else:
			raise StreamsDoNotSupportDownload()
	
	def download(self, language: int) -> None:
		raise NotImplementedError()
		s: Stream = self.get_best_download_stream(language)
		os.makedirs(f"./downloads/{self.anime_work_title}", exist_ok=True)
		s.download(f"./downloads/{self.anime_work_title}/{self.anime_work_title}_S{str(self.season_number).rjust(2, '0')}_E{str(self.episode_number).rjust(2, '0')}.mp4")

class Anime:
	def __init__(self, url:str) -> None:
		self.RESPONSE: requests.Response = requests.get(url)
		self.RAW_DATA: xmltodict.OrderedDict[str, json.Any] = xmltodict.parse(re.sub(r"<script(\w|\W)*?>(\w|\W)+?</(no)?script>", "", Bs(requests.get(url).text, features="html.parser").__str__())) #type: ignore
		self.url: str = url
		self.work_title: str = re.search(r"(?<=stream\/)[^\/\s]+", url).group() # type: ignore

		pot_movie: dict[str, str] = self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][1]["ul"][0]["li"][1]["a"] #type: ignore
		self.movie_page: str | None = pot_movie["@href"] if "film" in pot_movie["#text"].lower() else None #type: ignore
		self.season_pages: list[str] = [
			e["a"]["@href"] for e in self.RAW_DATA["html"]["body"]["div"]["div"]["div"][1]["div"][1]["ul"][0]["li"][1:] if not ("film" in e["a"]["#text"].lower()) #type: ignore
		]
		self.seasons: list[Season] = [ Season("https://aniworld.to"+u) for u in self.season_pages ]
	
	def get_all_episodes(self) -> list[Episode]:
		all_episodes: list[Episode] = []
		for s in self.seasons:
			all_episodes.extend(s.episodes)
		return all_episodes

	def __to_json__(self) -> dict[str, typing.Any]:
		return {
            "url": self.url,
			"seasons": [s.__to_json__() for s in self.seasons],
			"work_title": self.work_title
		}
	
	def download(self, language: int) -> None:
		executor = futures.ThreadPoolExecutor()
		jobs: list[Episode] = []
		for s in self.seasons:
			for e in s.episodes:
				jobs.append(e)
		workers: list[futures.Future[None]] = [executor.submit(e.download, language) for e in jobs]
		pbar = tqdm.tqdm(workers, total=len(jobs), position=0, ascii=".#", colour="#00ff00")
		for _ in futures.as_completed(workers):
			pbar.update()