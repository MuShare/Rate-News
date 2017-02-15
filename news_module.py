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


cover_default = "http://thietbidetnhuom.com/upload/images/tin-tuc.jpg"

class Crawler_FX168(util.Crawler):
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
		newsList = html.find("div", { "class" : "yjl_zixunList" })
		print len(newsList)
		for li in newsList.find_all("li"):
			# print "section"
			for a in li.find_all('a'):
				link = a.get('href')
				print link
				urlList.append({"link": link, "cover": a.find("img").get("src")})

	def getNews(self, url):
		'''
		Get news content from a url
		return news content: attribute json
		'''
		# article element 
		html = self.getSoupContent(url["link"]).find("div", {"class": "yjl_rili_content"})
		# article splited to title, pubdate, source, cover, link, lan, content
		title = html.find("h1").get_text()
		info = html.find("h3").find_all("span")
		pubdate = info[1].get_text()
		source = info[2].get_text()
		cover = url["cover"]
		link = url
		lan = "zh-cn"
		content = []
		contentSoup = html.find("div", {"class": "TRS_Editor"})
		for element in contentSoup.find_all():
			if element["align"] == 'justify':
				content.append({"type": "para", "value": element.get_text()})
			elif element["align"] == 'center':
				relaUrl = element.find("img").get("src")
				img = self.imageAbsolutePath(link) + relaUrl[1:]  
				content.append({"type": "image", "value": img})

		return News(title, pubdate, source, cover, link, lan, content)

	def imageAbsolutePath(self, url):
		
		i = len(url) - 1
		while i >= 0:
			if url[i] == '/':
				break;
			i -= 1
		return url[:i]
	def do(self):
		url = "http://wap.fx168.com/m/news/"
		result = []
		for url in self.getNewsList(url):
			result.append(self.getNews(url))

		self.writeToFile("FX168NewsResult.txt", result)


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

class Crawler_yahoo(util.Crawler):
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
		# urls from page 1 to 5
		pages = []
		for i in range(5):
			pages.append(self.getSoupContent(url + str(i)))
		
		for html in pages:
			for li in html.find("ul", { "class" : "list" }).find_all("li"):
				link = li.a.get("href")
				# print "url:" + link
				global cover_default
				cover = cover_default
				hasCover = li.find("div", {"class": "thumb"})
				if hasCover is not None:
					cover = hasCover.img.get("src")

				urlList.append({"link": link, "cover": cover})
		return urlList

	def getNews(self, url):
		'''
		Get news content from a url
		return news content: attribute json
		'''
		# article element 
		print "url: " + url["link"]
		html = self.getSoupContent(url["link"]).find('article')
		# article splited to title, pubdate, source, cover, link, lan, content
		title = html.find("h1", { "class" : "title" }).get_text()
		pubdate = html.find("p", {"class": "subText"}).time.get_text()[:-2]
		source = html.find("p", {"class": "subText"}).a.get_text()
		cover = url["cover"]
		link = url["link"]
		lan = "ja"
		content = html.find("div", {"class": "pgraphWrap"}).find("p", {"class": "text"}).get_text()
		
		return util.News(title, pubdate, source, cover, link, lan, content)

	def do(self):
		url = "http://news.yahoo.co.jp/hl?c=bus&p="
		result = []
		for url in self.getNewsList(url):
			result.append(self.getNews(url))
		print type(result)
		self.writeToFile("yahooNewsResult.txt", result)

	


def main():
	crawler1 = Crawler_FX168()
	crawler1.do()

if __name__ == "__main__": main()