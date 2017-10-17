#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox


class Application(Frame):
	def __init__(self,master= None):
		Frame.__init__(self,master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.nameInput = Entry(self)
		self.nameInput.pack()
		self.alertButton = Button(self, text="submit", command = self.hello)
		self.alertButton.pack()
	def hello(self):
		name = self.nameInput.get() or 'libin'
		tkMessageBox.showinfo("message","hello %s" % name)
			

app = Application()
app.master.title("hello")
app.mainloop()			