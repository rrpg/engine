# -*- coding: utf-8 -*-

class exception(BaseException):
	def __init__(self, message='', code=1):
		BaseException.__init__(self, message)
		if code not in self.getCodes():
			raise ValueError('Unknown error code')
		self.code = code

	def getCodes(self):
		return (1,)
