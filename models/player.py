# -*- coding: utf-8 -*-

import sys
import core.exception
from models import character
from models.Model import Model
import datetime
from models.settings import settings
from core.localisation import _


class player(character.character):
	def __init__(self):
		self._model = None

	def isConnected(self):
		return self._model is not None

	#~ Method to connect the player
	def connect(self, login):
		self._login = login
		self._model = model.loadByLogin(self._login)

		if len(self._model) == 0:
			self._login = None
			raise exception(_('ERROR_CONNECT_INVALID_CREDENTIALS'))

		return True

	def createNewPlayer(self, login, speciesId, genderId):
		self._model = {
			'login': login,
			'name': login,
			'id_species': speciesId,
			'id_gender': genderId,
			'id_area': settings.get('START_CELL_ID')
		}

		self._model['id_character'] = character.model.insert(self._model)
		model.insert(self._model)


class model(character.model):
	fields = ['id_player', 'login', 'id_character']

	@staticmethod
	def loadByLogin(login):
		pm = model.loadBy({'login': login})

		if len(pm) == 0:
			return dict()

		pm = pm[0]
		cm = character.model.loadById(pm['id_character'])
		cm.update(pm)

		return cm


class exception(core.exception.exception):
	pass
