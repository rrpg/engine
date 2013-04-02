# -*- coding: utf8 -*-

from AreaModel import AreaModel


class Area:
	@staticmethod
	def getByIdCHaracterAndDirection(idCharacter, direction):
		model = AreaModel.loadByIdCHaracterAndDirection(idCharacter, direction)

		if model is None:
			return None
		else:
			area = Area()
			area._model = model
			return area
