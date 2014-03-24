# -*- coding: utf-8 -*-

import sys
import getpass
import core.exception
from core import utils
from models import gender, species, character
from models.Model import Model
import datetime
from models.settings import settings
from core.localisation import _


class player(character.character):
	def __init__(self, login, password):
		self._login = login
		self._password = password
		self._model = None

	def isConnected(self):
		return self._model is not None

	#~ Connect the player by asking him to enter his login and his password
	def loadPlayerFromStdIn(self):
		if self._login is None or self._password is None:
			self._readLoginAndPassword(False, False)

	#~ Method to connect the player
	def connect(self):
		self._model = model.loadByLoginAndPassword(self._login, self._password)

		if len(self._model) == 0:
			self._login = None
			self._password = None
			raise exception(_('ERROR_CONNECT_INVALID_CREDENTIALS'))

		return True

	#~ Read the login and the password from stdin
	def _readLoginAndPassword(self, checkLogin, askConfirmPassword):
		while self._login is None or self._login == '':
			self._login = utils.read(_('LOGIN_PROMPT'))

			if checkLogin and len(model.loadBy({'login': self._login})):
				print(_('ERROR_SIGNUP_LOGIN_ALREADY_USED'))
				self._login = None

		confirmPassword = ''
		while (self._password is None or self._password == ''):
			self._password = getpass.getpass(_('PASSWORD_PROMPT'))

			if askConfirmPassword is True:
				confirmPassword = getpass.getpass(_('CONFIRM_PASSWORD_PROMPT'))
			else:
				confirmPassword = self._password

			if self._password != confirmPassword:
				print(_('ERROR_SIGNUP_PASSWORDS'))
				self._password = None

	def createNewPlayerFromStdIn(self):
		self._readLoginAndPassword(True, True)

		genders = gender.model.loadAll()
		nbGenders = len(genders)

		print(_('GENDER_SELECTION'))
		for k, v in enumerate(genders):
			print(str(k).rjust(3) + ' - ' + v['name'])

		g = -1
		while g < 0 or g >= nbGenders:
			g = utils.read(_('GENDER_PROMPT'))
			try:
				g = int(g)
			except:
				g = -1

		genderId = genders[g]['id_gender']

		sps = species.model.getSpecies()
		nbSpecies = len(sps)

		if nbSpecies == 1:
			speciesId = sps[0]['id_species']
		else:
			print(_('SPECIES_SELECTION'))
			for k, v in enumerate(sps):
				print(str(k).rjust(3) + ' - ' + v['name'])
				print(v['description'])

			sp = -1
			while sp < 0 or sp >= nbSpecies:
				sp = utils.read(_('SPECIES_PROMPT'))
				try:
					sp = int(sp)
				except:
					sp = -1

			speciesId = sps[sp]['id_species']

		self._model = {
			'login': self._login,
			'name': self._login,
			'password': self._password,
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
