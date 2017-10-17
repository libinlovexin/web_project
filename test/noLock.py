#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time,threading

balance = 0

def change(n):
	global balance
	balance = balance + n
	balance = balance -n

def runThread(n):
	for i in range(1000):
		change(n)

if __name__ == '__main__':
	t1 = threading.Thread(target = runThread , args = (5,))
	t2 = threading.Thread(target = runThread , args = (7,))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	print balance

