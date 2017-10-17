#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Chain(object):
	def __init__(self,path=''):
		self._path = path

	def __getattr__(self,value):
		return Chain('%s/%s' % (self._path,value))

	def user(self,name):
		return Chain('%s/user/%s' % (self._path,name))

	def __str__(self):
		return self._path

	__repr__ = __str__

print Chain().status.users.timeline.list #/status/user/timeline/list
print Chain().user('michael').timeline.test
				