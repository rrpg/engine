# -*- coding: utf8 -*-

from Model import Model


class character:
	@staticmethod
	def searchByNameAndIdArea(name, idArea):
		m = model.loadBy({'name': name, 'id_area': idArea})
		return character.loadFromModel(m[0])

	@staticmethod
	def searchByIdArea(idArea):
		models = model.loadBy({'id_area': idArea})
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


class exception(BaseException):
	pass
