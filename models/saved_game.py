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
					'id_character': None,
					'snapshot_player': None
				},
				('id_saved_game = ?', [saveId])
			)
			player.model.delete(
				('id_player = ?', [savedGame['id_player']])
			)
			character.model.delete(
				('id_character = ?', [savedGame['id_character']])
			)

	@staticmethod
	def parseSavedGames(savedGames):
		ret = {
			'has_existing_games': False,
			'saved_games': []
		}
		for s in savedGames:
			if s['id_player'] is None:
				save = s
			else:
				save = player.player.decodeSnapshot(s['snapshot_player'])
				save['id_saved_game'] = s['id_saved_game']
				ret['has_existing_games'] = True
			ret['saved_games'].append(save)

		return ret

class model(Model):
	"""
	Class to interact with the values in the database.
	"""

	fields = (
		'id_saved_game',
		'id_player',
		'id_character',
		'snapshot_player'
	)


class exception(core.exception.exception):
	pass
