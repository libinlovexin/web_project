#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

class lastUpdateOrderedDict(OrderedDict):

	def __init__(self,max):
		super(lastUpdateOrderedDict,self).__init__()
		self._max = max

	
	def __setitem__(self,key,value):
		containsKey = 1 if key in self else 0
		#假如超过长度，删除第一个进入的元素
		if len(self) - containsKey >= self._max:
			last = self.popitem(last =False)
			print "remove:" , last
		if containsKey:
			del self[key]
			print "set :" , (key , value)
		else:
			print "add : ", (key, value)
		#调用夫类set方法
		OrderedDict.__setitem__(self,key,value)


if __name__ == '__main__':
	a = lastUpdateOrderedDict(2)
	a["x"] = 1
	a["z"] = 12
	a["aa"] = 14
	print a						