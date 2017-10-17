#!/usr/bin/env python
# -*- coding: utf-8 -*-


def upFirst(x):
	if not 	isinstance(x,(str)):
		raise TypeError("please enter a str")
	if len(x)<2:
	  raise TypeError("str is too short")

	return x[0].upper() + x[1:].lower()


if __name__ == '__main__':
	result = map(upFirst,['adam', 'LISA', 'barT'])
	print result	  	
