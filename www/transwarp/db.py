#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Rockee'

"""
设计db模块的原因：
	1.操作数据库简单
		一次数据访问： 数据库链接 => 游标对象 => 执行SQL => 处理异常 => 清理资源
		db模块对过程进行封装，使用户只需要关注sql执行

	2.数据安全
	  因为每个链接请求是无关性的，有多个线程或者进程请求数据的时候，容易混乱
	  所以数据链接对象以ThreadLocal对象传入
设计DB接口：
	1.设计原则：
		简单易用的api接口
	2.调用接口：
		1.初始化数据库链接信息
			create_engine封装了如下功能：
				1.为数据库连接 准备需要的配置信息
				2.创建数据库链接（由生成的全局对象engine的 connect方法提供）
				from transwarp import db
				db.create_engine(user = 'root',
												 password = 'password',
												 database = 'test',
												 host = '127.0.0.1'
												 port = 3306)		  	 
		
		2.执行SQL DML
			select 函数封装了如下功能
				1.支持一个数据库链接里执行多个SQL语句
				2.支持连接的自动获取和释放
			使用样例：
				users = db.select('select * from user')
				              # users =>
              # [
              #     { "id": 1, "name": "Michael"},
              #     { "id": 2, "name": "Bob"},
              #     { "id": 3, "name": "Adam"}
              # ]
    3.支持事务
    	transaction 函数封装了如下功能：
    		1.事务也可以嵌套，内层事务会自动合并到外层事务，这种事务模型满足99%的需求
  """
import time,uuid,functools,threading,logging

#创建全局引擎对象
engine = None


class Dict(dict):
	"""    
	实现一个简单的可以通过属性访问的字典，比如 x.key = value

	"""
	def __init__(self,name=(),value=(),**kw):
		super(Dict,self).__init__(self,**kw)
		for k,v in zip(name,value):
			self[k] = v

	def __setattr__(self,k,v):
		self[k] = v

	def __getattr__(self,k):
		try:
			return self[k]
		except KeyError:
			raise AttributeError(r" 'Dict' has no attribute %s " % k)				
