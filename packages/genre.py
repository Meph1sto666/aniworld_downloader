import json

class Genre:
    def __init__(self, name:str, mainGenre:bool=False) -> None:
        self.MAIN_GENRE = mainGenre
        self.NAME = name.lower()
    def __str__(self) -> str:
        j = {
            "name": self.NAME
        }
        if self.MAIN_GENRE:
            j["main_genre"] = self.MAIN_GENRE
        return json.dumps(j)