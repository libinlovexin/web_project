#!/usr/bin/env python
# -*- coding: utf-8 -*-

import decorator


class Student(object):
	
	@property		
	def score(self):
		return self._score

	@score.setter
	def score(self,score):
		if 1<score<=100:
			self._score = score
		else:
			raise ValueError("error score")		
	@property	
	def name(self):
		return self._name

	@name.setter	
	def name(self,name):
		if isinstance(name,str):
			self._name = name
		else:
			raise TypeError("error name")



if __name__ == '__main__':
	student = Student()
	student.score = 101
	student.name = 'rockee'
	print student.score									
