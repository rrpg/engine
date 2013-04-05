# -*- coding: utf8 -*-

from Model import Model


class character:
	@staticmethod
	def searchByNameAndPlayer(name, player):
		m = model.loadByNameAndIdPlayer(
			name, player.getModel().getPk()
		)
		return character.loadFromModel(m)

	@staticmethod
	def searchByPlayer(player):
		models = model.loadNeighboursFromIdCharacter(
			player.getModel().getIdCharacter()
		)
		chars = list()
		for m in models:
			chars.append(character.loadFromModel(m))
		return chars

	@staticmethod
	def loadFromModel(m):
		if m is None:
			return None
		else:
			c = character()
			c._model = m
			return c

	def getId(self):
		return self._model.getPk()

	def goTo(self, idArea):
		self._model.setIdArea(idArea)
		self._model.savePosition()


class model(Model):
	fields = ['id_character', 'name', 'id_species', 'id_gender', 'id_area']
	def __init__(self, idCharacter=None):
		super(model, self).__init__()
		if idCharacter is not None:
			self._characterFields = model.getCharacterInfosFromId(
				idCharacter
			)
		else:
			self._characterFields = dict()

	#public
	def setSpecies(self, species):
		self._characterFields["id_species"] = str(species)

	def setGender(self, gender):
		self._characterFields["id_gender"] = str(gender)

	def setName(self, name):
		self._characterFields["name"] = name

	def setIdArea(self, idArea):
		self._characterFields["id_area"] = idArea

	def getName(self):
		return self._characterFields["name"]

	def getIdArea(self):
		return self._characterFields["id_area"]

	def getPk(self):
		return self._characterFields["id_character"]

	def save(self):
		if 'id_character' not in self._characterFields:
			self.__setPk(Model.insert("character", self._characterFields))
		else:
			Model.update(
				"character",
				self._characterFields,
				('id_character = ?', [self._characterFields['id_character']])
			)

		return True

	def savePosition(self):
		Model.update(
			"character",
			{'id_area': self._characterFields['id_area']},
			('id_character = ?', [self._characterFields['id_character']])
		)

	@staticmethod
	def _createFromData(data):
		if len(data) == 0:
			return None
		else:
			m = model()
			m._setPk(data['id_character'])
			m.setName(data['name'])
			m.setSpecies(data['id_species'])
			m.setGender(data['id_gender'])
			m.setIdArea(data['id_area'])

			return m

	@staticmethod
	def loadByIdCharacter(idChar):
		c = model.getCharacterInfosFromId(idChar)
		return model._createFromData(c)

	@staticmethod
	def getCharacterInfosFromId(idCharacter):
		query = "\
			SELECT\
				id_character,\
				name,\
				id_species,\
				id_gender,\
				id_area\
			FROM\
				`character`\
			WHERE\
				id_character = ?\
			"

		return Model.fetchOneRow(query, [idCharacter])

	@staticmethod
	def loadByNameAndIdPlayer(name, playerId):
		character = {}

		query = "\
			SELECT\
				c1.id_character,\
				c1.name,\
				c1.id_species,\
				c1.id_gender,\
				c1.id_area\
			FROM\
				`character` AS c1\
				JOIN character AS cp ON cp.id_area = c1.id_area\
				JOIN player ON id_player = ?\
					AND player.id_character = cp.id_character\
			WHERE\
				c1.name = ?\
			LIMIT 1"

		c = Model.fetchOneRow(query, [playerId, name])
		return model._createFromData(c)

	@staticmethod
	def loadNeighboursFromIdCharacter(characterId):
		character = {}

		query = "\
			SELECT\
				c1.id_character,\
				c1.name,\
				c1.id_species,\
				c1.id_gender,\
				c1.id_area\
			FROM\
				character AS c1\
				JOIN character AS cp ON\
					cp.id_area = c1.id_area\
					AND cp.id_character = ?\
					AND cp.id_character != c1.id_character\
			"

		cModels = list()
		characters = Model.fetchAllRows(query, [characterId])
		for c in characters:
			cModels.append(model._createFromData(c))
		return cModels

	#protected:
	def _setPk(self, pk):
		self._characterFields["id_character"] = str(pk)

	__setPk = _setPk


class exception(BaseException):
	pass
