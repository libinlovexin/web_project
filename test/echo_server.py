#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket,time,threading

def tcplink(sock,addr):
	print "Accrept a new connection from %s:%s " % addr
	sock.send("welcome")
	while True:
		data = sock.recv(1024)
		time.sleep(5)
		if data == 'exit' or not data:
			break
		sock.send('hello %s !' % data )
	sock.close()
	print 'Connection from %s:%s closed' % addr	
			

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(('127.0.0.1',9999))

s.listen(5)

print "waiting for connection ...."

while True:
	sock,addr = s.accept()
	#创建线程
	t  = threading.Thread(target = tcplink, args=(sock,addr))
	t.start()


	