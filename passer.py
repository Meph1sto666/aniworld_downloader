import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from packages import anime
from packages.data_analyser import getContent
import pypasser

# redirectId = "1170873"
# redirectUrl = "https://aniworld.to/redirect/1125332"
addToken = "?token="


a = anime.load(1582)
for i in range(0,1):
	redirectUrl = a.SEASONS[0].EPISODES[i].STREAMS[0].REDIRECT_URL
	redirectId = a.SEASONS[0].EPISODES[i].STREAMS[0].REDIRECT_ID
	try:
		browser = webdriver.Firefox()
	except:
		browser = webdriver.Chrome()
	browser.get(redirectUrl)
	i = 0
	token = ""
	while (redirectId in browser.current_url):
		time.sleep(1)
		iframe = browser.find_elements(By.TAG_NAME, "iframe")[0]
		browser.switch_to.frame(iframe)
		token = browser.find_element(By.XPATH,"/html/body/input").get_attribute("value")
		browser.switch_to.default_content()
		
		# browser.current_url = redirectUrl + addToken + token
		# browser.get(redirectUrl + addToken + token)
	browser.close()