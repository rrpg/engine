# -*- coding: utf8 -*-

from Model import Model


class model(Model):
	fields = ['id_species', 'description', 'name_m', 'name_f']

	@staticmethod
	def getSpecies():
		fields = {'id_species': 'id_species', 'description': 'description', 'name': 'name'}
		return model.loadAll(fields)
