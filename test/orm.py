#!/usr/bin/env python
# -*- coding: utf-8 -*-

'Orm simple class'

__author__ = 'rockee'

#字段基类
class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
  def __init__(self, name):
    super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):
  def __init__(self, name):
    super(IntegerField, self).__init__(name, 'bigint')

class TextField(Field):
	def __init__(self, name):
		super(TextField,self).__init__(name, 'text')

#Model元类 
class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings = dict()
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = name # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)

#Model类
class Model(dict):
	__metaclass__ = ModelMetaclass
	
	def __init__(self,**kv):
		super(Model,self).__init__(self,**kv)

	def __getattr__(self,k):
		try:
			return self[k]
		except KeyError:
			raise AttributeError(r"'Model' has none attribute %s" % k)

	def __setattr__(self,k,value):
		self[k] = value

	def save(self):
		fields = []
		params = []
		args = []
		for k,v in self.__mappings__.iteritems():
			fields.append(v.name)
			params.append("?")
			args.append(getattr(self,k,None))
			sql = 'insert into %s (%s) values (%s) ' % (self.__table__,','.join(fields),','.join(fields))
			print 'sql: %s' % sql
			print 'args: %s' % str(args)

	
class User(Model):
    id = IntegerField('uid')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')
    content  = TextField('content')

u = User(id='12345', name='Michael', email='test@orm.org', password='my-pwd',content='sasasasasasas')
u.save()			 					
		
