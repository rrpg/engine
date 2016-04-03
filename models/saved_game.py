# -*- coding: utf-8 -*-

import core
from models.Model import Model
from models import character, player
import sqlite3


class saved_game:
	@staticmethod
	def loadAll():
		return model.loadAll()

	@staticmethod
	def loadById(savedGameId):
		savedGame = model.loadById(savedGameId)
		if savedGame == {}:
			return None
		return savedGame

	@staticmethod
	def updateSavedGame(saveId, data):
		model.update(data, ('id_saved_game = ?', [saveId]))

	@staticmethod
	def cleanSavedGame(saveId):
		savedGame = model.loadById(saveId)
		if savedGame['id_player'] is not None:
			model.update(
				{
					'id_player': None,
					'id_character': None
				},
				('id_saved_game = ?', [saveId])
			)
			player.model.delete(
				('id_player = ?', [savedGame['id_player']])
			)
			character.model.delete(
				('id_character = ?', [savedGame['id_character']])
			)

class model(Model):
	"""
	Class to interact with the values in the database.
	"""

	fields = (
		'id_saved_game',
		'id_player',
		'id_character'
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


class exception(core.exception.exception):
	pass
