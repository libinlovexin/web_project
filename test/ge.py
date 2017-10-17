#!/usr/bin/env python

def fib(max):
	n,a,b = 0,0,1
	while n < max:
		yield a
		a,b = b,a+b
		n = n+1


def test(start,end):
	print [x for i,x in enumerate(fib(end)) if i >= start]


test(0,100)

