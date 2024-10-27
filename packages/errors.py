class StreamsDoNotSupportDownload(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
		
class InvalidStreamURL(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)