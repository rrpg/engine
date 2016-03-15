# -*- coding: utf-8 -*-

from models.Model import Model

class settings(Model):
	fields = ('id_setting', 'key', 'value')

	@staticmethod
	def get(key):
		try:
			val = settings.loadBy({'key': key}, ['value'])
			if val is None:
				val = []
			return val[0]['value']
		except IndexError as e:
			raise IndexError("Unknown key " + key + " in the settings")

