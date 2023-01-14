import json

class Stream:
	def __init__(self, redirectId:int, host:str, language:str) -> None:
		self.HOST = host
		self.REDIRECT_ID = redirectId
		self.LANGUAGE = language

	def __json__(self) -> dict:
		return {
			"host": self.HOST,
			"redirect_id": self.REDIRECT_ID,
			"language": self.LANGUAGE
		}
	def __str__(self) -> str:
		return json.dumps(self.__json__())