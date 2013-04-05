# -*- coding: utf8 -*-

import sys
import getpass
import utils
import gender
import species
import character
from Model import Model
import datetime

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
		self._model = model.loadByLoginAndPassword(
			self._login, self._password
		)

		if self._model is None:
			self._login = None
			self._password = None
			raise exception("Invalid login or password")

		return True

	#~ Read the login and the password from stdin
	def _readLoginAndPassword(self, checkLogin, confirmPassword):
		while self._login is None or self._login == '':
			self._login = utils.read("Login: ")

			if checkLogin and model.loadByLogin(self._login) is not None:
				print('This login is already used')
				self._login = None

		confirmPassword = ''
		while (self._password is None or self._password == ''):
			self._password = getpass.getpass("Password: ")

			if confirmPassword:
				confirmPassword = getpass.getpass("Confirm password: ")
			else:
				confirmPassword = self._password

			if self._password != confirmPassword:
				print('The passwords do not match')
				self._password = None

	def createNewPlayerFromStdIn(self):
		self._readLoginAndPassword(True, True)

		genders = gender.model.loadAll()
		nbGenders = len(genders)

		for k, v in enumerate(genders):
			print(v['name'] + " (" + str(k) + ")")

		g = -1
		while g < 0 or g >= nbGenders:
			g = utils.read("Character gender: ")
			try:
				g = int(g)
			except:
				g = -1

		genderId = genders[g]['id_gender']

		sps = species.model.getSpecies(genders[g]['name'])
		nbSpecies = len(sps)

		for k, v in enumerate(sps):
			print(v['name'] + " (" + str(k) + ")")
			print(v['description'])

		sp = -1
		while sp < 0 or sp >= nbSpecies:
			sp = utils.read("Character species: ")
			try:
				sp = int(sp)
			except:
				sp = -1

		speciesId = sps[sp]['id_species']

		self._model = model()
		self._model.setLogin(self._login)
		self._model.setPassword(self._password)
		self._model.setSpecies(speciesId)
		self._model.setGender(genderId)
		self._model.save()
		self.goTo(1)

	def getModel(self):
		return self._model


class model(character.model):
	fields = ['id_player', 'login', 'password', 'id_character', 'date_creation']
	def __init__(self, idCharacter=None):
		super(model, self).__init__(idCharacter)
		self._playerFields = dict()

	def getPk(self):
		return self._playerFields["id_player"]

	@staticmethod
	def loadByLoginAndPassword(login, password):
		query = "\
			SELECT\
				id_player,\
				login,\
				id_character\
			FROM\
				player\
			WHERE\
				login = ? AND password = ?\
		"

		m = Model.fetchOneRow(query, (login, password))

		if len(m) > 0:
			pm = model(m['id_character'])
			pm._setPk(m['id_player'])
			pm.setLogin(m['login'])
			pm.setIdCharacter(m['id_character'])
			return pm

		return None

	@staticmethod
	def loadByLogin(login):
		query = "\
			SELECT\
				id_player,\
				login,\
				id_character\
			FROM\
				player\
			WHERE\
				login = ?\
		"

		model = Model.fetchOneRow(query, [login])

		if len(model) > 0:
			pm = model(model['id_character'])
			pm._setPk(model['id_player'])
			pm.setLogin(model['login'])
			pm.setIdCharacter(model['id_character'])
			return pm

		return None

	def _setPk(self, pk):
		self._playerFields["id_player"] = pk

	def setLogin(self, login):
		self._playerFields["login"] = login

	def setIdCharacter(self, idCharacter):
		self._playerFields["id_character"] = idCharacter

	def getIdCharacter(self):
		return self._playerFields["id_character"]

	def setPassword(self, password):
		self._playerFields["password"] = password

	def save(self):
		self.setName(self._playerFields["login"])
		super(model, self).save()

		self._playerFields["date_creation"] = datetime.datetime.now()
		self._playerFields["id_character"] = character.model.getPk(self)

		if 'id_player' not in self._playerFields:
			self._setPk(model.insert(self._playerFields))
		else:
			model.update(
				self._playerFields,
				('id_player = ?', [self.getPk()])
			)

		return True


class exception(BaseException):
	pass
