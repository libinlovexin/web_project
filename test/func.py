#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from math import sqrt
from math import tan

'''
高阶函数的应用
'''

def same(num,*kw):
	if not isinstance(num,(int,float)):
		raise TypeError("bad number type")

	#初始化字典列表
	ref = {}
	#计算可变函数
	for func in kw:
		try:
			ref[func.__name__] = func(num)
		except ValueError:
			ref[func.__name__] = 'None'

	return ref

result = same(-10.5,abs,sqrt,tan)		
print result
