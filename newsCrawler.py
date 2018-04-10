# -*- coding: utf-8 -*-
import requests
import time
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pykafka import KafkaClient

HTML_PARSER   = "html.parser"
ROOT_URL      = 'https:'
USER_AGENT    = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
HEADERS       = {'User-Agent':USER_AGENT}
YAHOO_URL     = 'https://tw.news.yahoo.com'
POLITICS      = '/politics/archive/'
ENTERTAINMENT = '/entertainment/archive/'
CHROME_PATH   = "E:\selenium_driver_chrome\chromedriver.exe"
SCROLL_PAUSE_TIME = 0.5

client = KafkaClient(hosts="172.20.10.3:9092") #ali cloud server
topic  = None

def getNewsURL(categories):
	news_req = requests.get(YAHOO_URL+categories, headers = HEADERS)
	if news_req.status_code == requests.codes.ok:
		print('URL OK')
		driver = webdriver.Chrome(CHROME_PATH)
		driver.implicitly_wait(3)
		driver.get(YAHOO_URL+categories)
		element = driver.find_element_by_tag_name('html')
		for i in range(1,10):
			element.send_keys(Keys.END)
			#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(SCROLL_PAUSE_TIME)
		soup = BeautifulSoup(driver.page_source, HTML_PARSER)
		#soup = BeautifulSoup(news_req.content, HTML_PARSER)
		newsli_list = soup.select('.StreamMegaItem')
		for i in newsli_list:
			newsURL = i.select('a')[0].get('href')
			if newsURL.startswith('/poll'):
				break
			else:
				newsURL = YAHOO_URL+newsURL
				print(newsURL)
				content = getContent(newsURL).strip()
				print(content)
				if content != '':
					with topic.get_sync_producer() as producer:
						producer.produce(bytes(content,'utf-8'))
				else:
					print('no data')


def getContent(newsURL):
	content_req = requests.get(newsURL, headers = HEADERS)
	if content_req.status_code == requests.codes.ok:
		print('URL OK')
		soup1 = BeautifulSoup(content_req.content, HTML_PARSER)
		title = soup1.select('.canvas-header')[0].text
		print('title:',title)
		print('\n')
		article =""
		for i in soup1.select('p[class="canvas-atom canvas-text Mb(1.0em) Mb(0)--sm Mt(0.8em)--sm"]'):
			if re.match('更多|延伸閱讀|相關報導|Line讀者觀看影片【點我看】|【延伸閱讀】', i.text):
				break
			else:
				article += i.text
		return article



if __name__ == '__main__':
	if(sys.argv[1] == 'p'):
		topic = client.topics[b'politics3']
		getNewsURL(POLITICS)
	elif(sys.argv[1]=='e'):
		topic = client.topics[b'entertainment4']
		getNewsURL(ENTERTAINMENT)
	else:
		print("input topic")
