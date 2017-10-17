#!/usr/bin/env python
# -*- coding: utf-8 -*-


'test module hello'
__author__ ='Rockee Lee'

import sys

def test():
	args = sys.argv
	if(len(args)) == 1:
		print "Hello World"
	elif(len(args) == 2):
		print "Hello %s" % args[1]
	else:
		print "Too many params"

if __name__ == '__main__':
	test()				

