#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

regex = re.compile('(.+).[^.]+') #不包含拓展名

def search(key,dir=os.path.abspath('.')):
	for i in os.listdir(dir):
		path = os.path.join(dir,i)
		fileName = re.search(regex,i)
		if os.path.isfile(path) and key in str(fileName.group(1)):
			print path
		if os.path.isdir(path):		
			search(key,path)

search('test','libin')