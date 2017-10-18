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


def next_id(t=None):
	"""
	生成一个唯一的id，t通过时间戳+随机数来生成
	""" 
	if t is None:
		t=time.time()
	return '%015d%s000' % (int(t*1000),uuid.uuid4().hex)


def _profiling(start,sql=''):
	"""
	根据start时间计算sql执行时间
	"""
	t = time.time() - start
	if t > 0.1:
		logging.warning("[PROFILING][DB] %s: %s  " % (t.sql))
	else:
		logging.info("[PROFILING][DB] %s: %s  " % (t.sql))

class DBError(Exeption):
	pass

class MultiColumnsError(DBError):
	pass

#创建全局引擎对象
engine = None

class _Engine(object):
	"""
	数据库引擎对象，
	用户保存db对象的函数，create_engine创建数据库链接
	"""
	def __init__(self,connect):
		self._connect = connect

	def connet(self):
		return self._connect()	


def create_engine(user,password,database,host='127.0.0.1',port=3306,**kw):
	"""
	db核心函数，用于创建数据库链接
	数据库链接对象保存在engine里
	"""
	import mysql.connector
	global engine
	if engine is not None:
		raise DBError("engine is already intialized") 
	params = dict(user = user, password = password,database = database ,host = host, port=port)
	default = dict(use_unicode = True,charset = 'utf8',collation = 'utf8_general_ci',autocommit = False)
	for k,v in default.iteritems():
		params[k] = kw.pop(k,v)
	params.update(kw)
	params['buffered'] = True
	engine = _Engine(lambda: mysql.connector.connect(**params))	

	logging.info("Init mysql engine (%s) ok" % hex(id(engine)))

class _LasyConnection(object):
	"""
	惰性链接数据库，只有调用cursor对象时，才链接数据库获取链接
	"""
	def __init__(self):
		self.connection = None

	def cursor(self):
		if self.connection is None:
			_connection = engine.connect()
			logging.info('[CONNECTION] [OPEN] connection <%s>...' % hex(id(_connection)))
			self.connection = _connection
		return self.connection		

	def commit(self):
		self.connection.commit()

	def rollback(self):
		self.connection.rollback()

#丢弃链接
	def cleanup(self):
		if self.connection:
			_connection = self.connection
			logging.info('[CONNECTION] [CLOSE] connection <%s>...' % hex(id(connection)))
			_connection.close()


class _DbCtx(thread.local):
	    """
    db模块的核心对象, 数据库连接的上下文对象，负责从数据库获取和释放连接
    取得的连接是惰性连接对象，因此只有调用cursor对象时，才会真正获取数据库连接
    该对象是一个 Thread local对象，因此绑定在此对象上的数据 仅对本线程可见
    """
	def __init__(self):
		self.connection = None
		self.transactions = 0

	def is_init(self):
		return self.connection is not None
#初始化链接
	def init(self):
		self.connection = _LazyConnection()
		self.transactions = 0

	def cleanup(self):
		self.connection.cleanup()
		self.connection = None

	def cursor(self):
		self.connection.cursor()

#dbctx对象
_dbCtx = _DbCtx()

class _ConnectionCtx(object):
	    """
    因为_DbCtx实现了连接的 获取和释放，但是并没有实现连接
    的自动获取和释放，_ConnectCtx在 _DbCtx基础上实现了该功能，
    因此可以对 _ConnectCtx 使用with 语法，比如：
    with connection():
        pass
        with connection():
            pass
    """

  #装饰器进入方法  
  def __enter__(self): 
  	"""
  	获取一个惰性连接对象
  	"""
  	global _dbCtx
  	self.should_cleanup = False
  	if not _dbCtx.is_init():
  		_dbCtx.init()
  		self.shouid_cleanup = True
  	return self
  
  def __exit__(self,exctype, excvalue, traceback):
  	global _dbCtx
  	if self.shouid_cleanup:		
  		_dbCtx.cleanup()

class _TransactionCtx(object):
    """
    事务嵌套比Connection嵌套复杂一点，因为事务嵌套需要计数，
    每遇到一层嵌套就+1，离开一层嵌套就-1，最后到0时提交事务
    """
	def __enter__(self):
		global _dbCtx
		self.should_close_conn = False
		if not _dbCtx.is_init():
			_dbCtx.init()
			self.should_close_conn = True
		_dbCtx.transactions +=1
		logging.info('begin transaction...' if _db_ctx.transactions == 1 else 'join current transaction...')
		return self

	def __exit__(self,exctype, excvalue, traceback):
		global _dbCtx
		_dbCtx.transactions -=1
		try:
			if _dbCtx.transactions == 0:
				if exctype is None:
					self.commit()
				else:
					self.rollback()
		finally:
			if self.should_close_conn:
				_dbCtx.cleanup()						    

  def commit(self):
  	global _dbCtx
  	logging.info("commiting transactions")
  	try:
  		_dbCtx.connection.commit()
  		logging.info("commit ok")
  	except:
  		logging.warning("commit fail,try rollback")
  		_dbCtx.connection.rollback()
  		logging.info("rollback ok")
  	  raise 				
  
  def rollback(self):
  	global _dbCtx
  	logging.warning("rollback transactions")
  	_dbCtx.connection.rollback()
  	logging.info("rollback ok")

#装饰器transactions
def with_transaction(func):  
   """
    设计一个装饰器 替换with语法，让代码更优雅
    比如:
        @with_transaction
        def do_in_transaction():
    >>> @with_transaction
    ... def update_profile(id, name, rollback):
    ...     u = dict(id=id, name=name, email='%s@test.org' % name, passwd=name, last_modified=time.time())
    ...     insert('user', **u)
    ...     update('update user set passwd=? where id=?', name.upper(), id)
    ...     if rollback:
    ...         raise StandardError('will cause rollback...')
    >>> update_profile(8080, 'Julia', False)
    >>> select_one('select * from user where id=?', 8080).passwd
    u'JULIA'
    >>> update_profile(9090, 'Robert', True)
    Traceback (most recent call last):
      ...
    StandardError: will cause rollback...
    """
  @functools.wraps(func)
  def _wrapper(*args,**kw):
  	start = time.time()
  	with _TransactionCtx():
  		func(*args,**kw)
   	_profiling(start)
  return _wrapper

def with_connection(func):
	"""
	装饰器，    设计一个装饰器 替换with语法，让代码更优雅
    比如:
        @with_connection
        def foo(*args, **kw):
            f1()
            f2()
            f3()
	处理多个链接请求
	"""
	@functools.wraps(func)
	def _wrapper(*args,**kw):
		start = time.time()
		with _ConnectionCtx():
			func(*args,**kw)
		_profiling(start)
	return _wrapper		











