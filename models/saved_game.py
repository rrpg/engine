# -*- coding: utf-8 -*-

from models.Model import Model
import sqlite3


class saved_game:
	@staticmethod
	def loadAll():
		return model.loadAll()


class model(Model):
	"""
	Class to interact with the values in the database.
	"""

	fields = (
		'id_saved_game',
		'id_player'
	)

	@staticmethod
	def loadAll():
		query = "\
			SELECT\
				id_saved_game,\
				login\
			FROM\
				saved_game sg\
				LEFT JOIN player p\
					ON sg.id_player = p.id_player\
			ORDER BY id_saved_game\
			"

		return Model.fetchAllRows(query)
