# -*- coding: utf-8 -*-

from Model import Model

class settings(Model):
	fields = ('id_setting', 'key', 'value')

	@staticmethod
	def get(key):
		try:
			return settings.loadBy({'key': key}, ['value'])[0]['value']
		except IndexError as e:
			raise IndexError("Unknown key " + key + " in the settings")

