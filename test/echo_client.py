#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect(('127.0.0.1',9999))

#接收欢迎消息
print s.recv(1024)

for data in ['rockee','sunny','jackey']:
	s.send(data)
	print s.recv(1024)
s.send('exit')
s.close()	