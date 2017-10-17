#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

def log(func_arg):
	#
	if hasattr(func_arg,"__call__"):  #假如传入的是一个方法
		def wrapper(*args,**kw):
			print "call %s:" % func_arg.__name__
			return func_arg(*args,**kw)
		return wrapper	
	else:  #传入一个文本，要定义一个装饰器
		def decorator(func):
			def wrapper2(*args,**kw):
				print " %s %s():" % ( func_arg,func.__name__)
				return func(*args,**kw)
			return wrapper2
		return decorator


		
def log3(func_args):
	desc = 'only call'
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kw):
			print " begin function %s %s" % (func.__name__,desc)
			result = func(*args,**kw)
			print "end fucntion %s %s " % (func.__name__,desc)
			return result
		return wrapper
	if hasattr(func_args,"__call__"):
		return decorator(func_args)
	else:
		desc = func_args
		return decorator			


@log
def now1():
	pass

@log('rockee')
def now2():
	pass



def log2(func):
	@functools.wraps(func)
	def wrapper(*args,**kw):
		print " begin function %s" % func.__name__
		result = func(*args,**kw)
		print "end fucntion %s" % func.__name__
		return result
	return wrapper
	
@log2
@log3("libin is Rockee")
def now3():
	a =  [x*x for x in range(1,10)]
	print a

if __name__ == '__main__':
	now1()
	now2()
	now3()	











