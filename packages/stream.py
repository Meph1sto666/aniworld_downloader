class Stream:
	def __init__(self, redirectId:int, host:str, language:str) -> None:
		self.HOST = host
		self.REDIRECT_ID = redirectId
		self.LANGUAGE = language