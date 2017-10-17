#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

localStudent = threading.local() #设置threadLocal变量

def process_student():
	print "Hello %s in (%s)" % (localStudent.name,threading.current_thread().name)

def process_thread(name):
  localStudent.name = name
  process_student()

if __name__ == '__main__':
	t1 = threading.Thread(target = process_thread, args = ("Rockee",),name = "Thread-1")
	t2 = threading.Thread(target = process_thread, args = ("Sunny",) , name = "Thread-2")
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	 	
