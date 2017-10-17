#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time, sys, Queue
from multiprocessing.managers import BaseManager

#创建QueueManager接收
class QueueManager(BaseManager):
	pass

#绑定网络上的方法
QueueManager.register("get_task_queue")
QueueManager.register("get_result_queue")

#链接服务器
serverAddr = "127.0.0.1"
m = QueueManager(address = (serverAddr,5000),authkey = 'libin')
print "connect to server %s ...." % serverAddr
#链接
m.connect()
#获取两个Queue对象
taskQueue = m.get_task_queue()
resultQueue = m.get_result_queue()

for i in range(10):
	try:
		n = taskQueue.get(i)
		print "Run task %d * %d" % (n,n)
		r = "%d * %d = %d" % (n,n,n*n)
		time.sleep(2)
		resultQueue.put(r)
	except Queue.Empty:
		print "task queue is empty"
#处理结束
print "work exit"			