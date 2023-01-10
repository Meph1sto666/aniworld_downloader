import json
import os
import requests
from bs4 import BeautifulSoup as Bs

class Home:
    def __init__(self):
        self.response:requests.Response = requests.get(os.getenv("AW_URL_HOME"))
        