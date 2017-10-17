#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

def iscomp(x):
	def check(i):
		if not isinstance(i,(int)):
			raise TypeError("x is not a integer")
		if i <1:
			raise TypeError("x is out of range")
		if i <3:
		  return False

		upbd = int(math.sqrt(i))
		for t in range(2,upbd+1):
			if i%t == 0:
				return True
			else:
			  return False
	return filter(check,x)
			  

print iscomp(range(1,100))