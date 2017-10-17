#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint


class MyHTMLParser(HTMLParser):

	def __init__(self):
		self._count = 0
		self._data = dict()
		self._flag = None
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		if tag == 'h3' and attrs.__contains__(('class','event-title')):
			#新建一个数组
			self._count +=1
			self._data[self._count] = dict()
			self._flag = 'event-title'
		if tag == 'time':
			self._flag = tag
		if tag == 'span' and attrs.__contains__(('class','event-location')):
			self._flag = 'event-location'		

	def handle_data(self, data):
		if self._flag == 'event-title':
			print data
			self._data[self._count][self._flag] = data
		if self._flag == 'time':
			print data
			self._data[self._count][self._flag] = data
		if self._flag == 'event-location':
			print data
			self._data[self._count][self._flag] = data
		self._flag = None
	
	def show_event(self):
		for v in self._data.values():
			print v['event-title'],'\n',v['time'],'\n',v['event-location']		
			


html = ''
try:
		page = urllib.urlopen('https://www.python.org/events/python-events/')
		html = page.read()

		parser = MyHTMLParser()
		parser.feed(html)
		parser.show_event()
finally:
    page.close()
