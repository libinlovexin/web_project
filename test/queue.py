
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process, Queue
import os, time, random

def write(q):
	for value in ["A","B","C"]:
		print "Put %s to Queue " % value
		q.put(value)
		time.sleep(random.random())

def read(q):
	while True:
		value = q.get(True)
		print "Get value %s from Queue " % value

if __name__ =="__main__":
	print "Process have been start (%s) " % os.getpid()
	q = Queue()
	pw = Process(target = write,args =(q,) )
	pr = Process(target = read, args =(q,) )
	pw.start()
	pr.start()
	pw.join()
	pr.terminate()
