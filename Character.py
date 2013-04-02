# -*- coding: utf8 -*-

from CharacterModel import CharacterModel


class Character:
	@staticmethod
	def searchByNameAndPlayer(name, player):
		model = CharacterModel.loadByNameAndIdPlayer(
			name, player.getModel().getPk()
		)

		if model is None:
			return None
		else:
			character = Character()
			character._model = model
			return character

	def getId(self):
		return self._model.getPk()

	def goTo(self, idArea):
		self._model.setIdArea(idArea)
		self._model.savePosition()
