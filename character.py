# -*- coding: utf8 -*-

from Model import Model


class character:
	@staticmethod
	def searchByNameAndIdArea(name, idArea):
		m = model.loadBy({'name': name, 'id_area': idArea})
		return character.loadFromModel(m[0])

	@staticmethod
	def searchByPlayer(player):
		models = model.loadNeighboursFromIdCharacter(
			player._model['id_character']
		)
		chars = list()
		for m in models:
			chars.append(character.loadFromModel(m))
		return chars

	@staticmethod
	def loadFromModel(m):
		if len(m) == 0:
			return None
		else:
			c = character()
			c._model = m
			return c

	def getId(self):
		return self._model['id_character']

	def goTo(self, idArea):
		self._model['id_area'] = idArea
		model.savePosition(self._model['id_character'], self._model['id_area'])


class model(Model):
	fields = ['id_character', 'name', 'id_species', 'id_gender', 'id_area']

	@staticmethod
	def savePosition(idCharacter, idArea):
		model.update(
			{'id_area': idArea},
			('id_character = ?', [idCharacter])
		)

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

		return Model.fetchOneRow(query, [playerId, name])

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
			cModels.append(c)
		return cModels


class exception(BaseException):
	pass
