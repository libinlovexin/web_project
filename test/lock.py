#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time,threading

balance = 100

lock = threading.Lock()

def change(n):
	global balance
	balance = balance + n
	balance = balance - n

def runThread(n):
	for i in range(1000):
		lock.acquire() #加锁
		try:
			change(n)
		finally:
			lock.release() #释放锁

if __name__ == '__main__':
	t1 = threading.Thread(target = runThread, args=(5,))
	t2 = threading.Thread(target = runThread, args=(11,))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	print balance
