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

class Crawler(object):
    '''
    Parent class for crawler
    '''
    def __init__(self, url=""):
        self.url = url

    def getSoupContent(self, url):
        '''
        Function to get html content for a given url
        url: http link
        return: html content
        '''
        # definition for html, or no variable error
        # print "getSoupContent"
        html = None
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1')
        # if header is essential, request.add_header('Host', 'm.sohu.com')
        # request.add_header("Host", "3g.163.com")
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        try:            
            html = urllib2.urlopen(request)
            # print html.getcode()
        except socket.timeout, e:
            print "time out"
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        except request.exceptions.Timeout  as IndexError:
            print "something wrong!"
            sys.exit(1)
        else:
            pass

        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def writeToFile(self, filename, data):
        with open(filename, 'a') as f:
            for item in data:
                f.write(str(item))




class News(object):
    '''
    New class for JSON
    '''
    def __init__(self, title, pubdate, source, cover, link, lan, content):
        self.title = title        # title
        self.pubdate = pubdate # publication data
        self.source = source   # news press
        self.cover = cover     # cover image, absolute address
        self.link = link         # link url
        self.lan = lan           # language
        self.content = content # news content

    def __str__(self):
        return ("##########\n" \
        		+ "title:" + self.title + "\n" \
                + "pubdate:" + self.pubdate + "\n" \
                + "source:" + self.source + "\n" \
                + "cover image:" + self.cover + "\n" \
                + "link:" + self.link + "\n" \
                + "language:" + self.lan + "\n" \
                + "content:" + "\n" \
                + "##########\n").encode("utf-8")

    def getJSON(self):
        '''
        News data to attribute JSON
        return JSON 
        '''

        return 0

    __repr__ = __str__