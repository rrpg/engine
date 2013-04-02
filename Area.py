# -*- coding: utf8 -*-

from AreaModel import AreaModel


class Area:
	@staticmethod
	def getByIdCharacterAndDirection(idCharacter, direction):
		model = AreaModel.loadByIdCharacterAndDirection(idCharacter, direction)

		if model is None:
			return None
		else:
			area = Area()
			area._model = model
			return area
