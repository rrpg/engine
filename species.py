# -*- coding: utf8 -*-

from Model import Model


class model(Model):
	@staticmethod
	def getSpecies(gender):
		query = "\
			SELECT\
				id_species,\
				"
		if gender == "male":
			query += "name_m AS name,"
		else:
			query += "name_f AS name,"

		query += "\
				description\
			FROM\
				species\
		"

		return Model.fetchAllRows(query, {})
