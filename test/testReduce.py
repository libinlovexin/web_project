#!/usr/bin/env python
# -*- coding: utf-8 -*-

def prod(l):
	def f(x,y):
		return x*y
	print reduce(f,l)
	
if __name__ == '__main__':
	prod(range(1,10))

