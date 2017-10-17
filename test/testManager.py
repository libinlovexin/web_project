#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, time, Queue
from multiprocessing.managers import BaseManager


#设置任务队列和执行队列

taskQueue = Queue.Queue()

resultQueue = Queue.Queue()

class QueueManager(BaseManager):
	pass

#注册两个队列到网络上
QueueManager.register('get_task_queue',callable = lambda: taskQueue)
QueueManager.register('get_result_queue',callable = lambda: resultQueue)

#绑定端口5001
manager = QueueManager(address = ('127.0.0.1',5000), authkey = 'libin')
#启动Queue
manager.start()
#通过网络访问对象
task  = manager.get_task_queue()
result = manager.get_result_queue()
#放几个任务进去
for i in range(10):
	n = random.randint(0,1000)
	print "put task %d " % n
	task.put(n)
#从result队列读取数据
print "try to read from result"
for i in range(10):
	r = result.get(timeout = 5)
	print ("result is %s" % r)

manager.shutdown()