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
	def connect(self, login, password):
		self._login = login
		self._password = password
		self._model = model.loadByLoginAndPassword(self._login, self._password)

		if len(self._model) == 0:
			self._login = None
			self._password = None
			raise exception(_('ERROR_CONNECT_INVALID_CREDENTIALS'))

		return True

	def createNewPlayer(self, login, password, speciesId, genderId):
		self._model = {
			'login': login,
			'name': login,
			'password': password,
			'id_species': speciesId,
			'id_gender': genderId,
			'id_area': settings.get('START_CELL_ID')
		}

		self._model['id_character'] = character.model.insert(self._model)
		model.insert(self._model)


class model(character.model):
	fields = ['id_player', 'login', 'password', 'id_character']

	@staticmethod
	def loadByLoginAndPassword(login, password):
		pm = model.loadBy({'login': login, 'password': password})

		if len(pm) == 0:
			return dict()

		pm = pm[0]
		cm = character.model.loadById(pm['id_character'])
		cm.update(pm)

		return cm


class exception(core.exception.exception):
	pass
