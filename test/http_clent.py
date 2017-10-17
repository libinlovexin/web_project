#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
#建立一个socket链接
#创建Socket时，AF_INET指定使用IPv4协议，如果要用更先进的IPv6，就指定为AF_INET6。SOCK_STREAM指定使用面向流的TCP协议，这样，一个Socket对象就创建成功，但是还没有建立连接。
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.163.com',80))
#发送GET请求，HTTP协议必须先发送请求到服务端才能拿到请求
s.send('GET / HTTP/1.1\r\nHost: www.163.com\r\nConnection: close\r\n\r\n')
#通过buffer接收数据
buffer = []
while True:
	d = s.recv(1024) #一次接收1024字节
	if d:
		buffer.append(d)
	else:
		break
data = " ".join(buffer)

s.close()

#写入到文件  		
head, html = data.split('\r\n\r\n',1)
print head

with open('163.html','wb') as f:
	f.write(html)

f.close()	