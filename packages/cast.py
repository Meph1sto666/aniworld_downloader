import json

class Cast:
	def __init__(self, name:str, castType:str) -> None:
		self.NAME = name
		self.CAST_TYPE = castType.lower();
	def __json__(self) -> str:
		return {
			"name": self.NAME,
			"cast_type": self.CAST_TYPE
		}
	def __str__(self) -> str:
		return json.dumps(self.__json__())