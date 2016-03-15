# -*- coding: utf-8 -*-

from models.Model import Model

class settings(Model):
	fields = ('id_setting', 'key', 'value')

	@staticmethod
	def get(key):
		val = settings.loadBy({'key': key}, ['value'])
		if val is None or len(val) == 0:
			raise IndexError("Unknown key " + key + " in the settings")
		return val[0]['value']

