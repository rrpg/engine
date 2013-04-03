# -*- coding: utf8 -*-

from Model import Model


class model(Model):
	fields = ['id_species', 'description', 'name_m', 'name_f']

	@staticmethod
	def getSpecies(gender):
		fields = {'id_species': 'id_species', 'description': 'description'}
		if gender == "male":
			fields['name'] = "name_m"
		else:
			fields['name'] = "name_f"

		return model.loadAll(fields)
