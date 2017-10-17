#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time,threading

def loop():
	name = threading.current_thread().name
	print "thread %s is runnning" % name
	n = 0
	while n<5 :
		n = n+1
		print " thread %s >>> %s" % (name,n)
		time.sleep(2)
	print "thread %s is end " % name

print "thread %s is running " % threading.current_thread().name
t = threading.Thread(target = loop, name="LoopThread")
t.start()
t.join()
print "thread %s is end" % threading.current_thread().name	