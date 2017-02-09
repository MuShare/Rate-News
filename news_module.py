# -*- coding:utf-8 -*-
'''
Created on 2017.2.8
@author: xiaotang
@github:http://github.com/namidairo777
'''

import urllib2
import socket
import httplib
from bs4 import BeautifulSoup
import util

class Crawler_163(util.Crawler):
	'''
	Extends Crawler
	'''
	def getNewsList(self, url):
		'''
		Get News url list from news list page
		url
		return list[]
		'''
		urlList = []
		html = self.getSoupContent(url)
		for section in html.find_all("section"):
			print "section"
			for a in section.find_all('a'):
				link = a.get('href')
				print link
				urlList.append({"link": link, "cover": link.find("img").get("src")})

	def getNews(self, url):
		'''
		Get news content from a url
		return news content: attribute json
		'''
		# article element 
		html = self.getSoupContent(url["link"]).find('article')
		# article splited to title, pubdate, source, cover, link, lan, content
		title = html.find("h1", { "class" : "title" }).get_text()
		pubdate = html.find("span", {"class": "time js-time"}).get_text()
		source = html.find("span", {"class": "source js-source"}).get_text()
		cover = url["cover"]
		link = url
		lan = "zh-cn"
		content = []
		contentSoup = html.find("div", {"class": "content"}).find("div", {"class": "page js-page on"})
		for element in contentSoup.find_all():
			if element.name == 'p':
				content.append({"type": "para", "value": element.get_text()})
			elif element.has_attr("photo"):
				content.append({"type": "image", "value": element.find("a").get("href")})

		return News(title, pubdate, source, cover, link, lan, content)

	def do(self):
		url = "http://3g.163.com/touch/money"
		result = []
		for url in self.getNewsList(url):
			result.append(self.getNews(url))

		print result


class Crawler_sina(util.Crawler):
	'''
	Extends Crawler
	'''
	def getNewsList(self, url):
		'''
		Get News url list from news list page
		url
		return list[]
		'''
		urlList = []
		html = self.getSoupContent(url)
		for article in html.find_all("article", { "class" : "article single-pic" }):
			link = article.get('data-original-url')
			print link
			urlList.append({"link": link, "cover": "http:" + link.find("img").get("src")})

	def getNews(self, url):
		'''
		Get news content from a url
		return news content: attribute json
		'''
		# article element 
		html = self.getSoupContent(url["link"]).find("section", { "class" : "module-article" })
		# article splited to title, pubdate, source, cover, link, lan, content
		title = html.find("h1", { "class" : "title" }).get_text()
		source = html.find("a", {"class": "source"}).get_text()
		pubdate = html.find("div", {"class": "extra-info"}).get_text()[:-len(source)]
		
		cover = url["cover"]
		link = url
		lan = "zh-cn"
		content = []
		contentSoup = html.find("article", {"class": "main-body"})
		for element in contentSoup:
			if element.name == 'p':
				content.append({"type": "para", "value": element.get_text()})
			elif element.name == "img":
				content.append({"type": "image", "value": "http:" + element.get("src")})

		return News(title, pubdate, source, cover, link, lan, content)

	def do(self):
		url = "http://finance.sina.cn/"
		result = []
		for url in self.getNewsList(url):
			result.append(self.getNews(url))


def main():
	crawler1 = Crawler_sina()
	crawler1.do()

if __name__ == "__main__": main()