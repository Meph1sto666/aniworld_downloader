from selenium import webdriver
import time;

url = "https://aniworld.to/redirect/1330714"
try:
	browser = webdriver.Firefox()
except:
	browser = webdriver.Chrome()
browser.get(url)
while (browser.current_url == url):
    time.sleep(1)
streamUrl = browser.current_url
browser.close()

print(streamUrl)