# -*- coding: utf8 -*-

from Model import Model


class model(Model):
	@staticmethod
	def getGenders():
		query = "\
			SELECT\
				id_gender,\
				name\
			FROM\
				gender\
		"

		return Model.fetchAllRows(query, {})
