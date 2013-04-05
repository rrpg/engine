# -*- coding: utf8 -*-

from Model import Model


class area:
	@staticmethod
	def getByIdCharacterAndDirection(idCharacter, direction):
		m = model.loadByIdCharacterAndDirection(idCharacter, direction)

		if len(m) == 0:
			return None
		else:
			a = area()
			a._model = m
			return a

	@staticmethod
	def getSurroundingAreas(idArea):
		return model.getSurroundingAreas(idArea)


class model(Model):
	@staticmethod
	def loadByIdCharacterAndDirection(idCharacter, direction):
		if direction not in ('north', 'south', 'east', 'west'):
			raise exception('Unknown direction')

		query = "\
			SELECT\
				ad.id_area,\
				ad.id_region,\
				ad.id_next_area_north,\
				ad.id_next_area_east,\
				ad.id_next_area_south,\
				ad.id_next_area_west\
			FROM\
				area AS ad\
				JOIN area AS ap ON ad.id_area = ap.id_next_area_%s\
				JOIN character AS c ON c.id_area = ap.id_area\
			WHERE\
				id_character = ?\
		" % direction

		return Model.fetchOneRow(query, [idCharacter])

	@staticmethod
	def getSurroundingAreas(idArea):
		query = "\
			SELECT\
				id_next_area_north IS NOT NULL AS north,\
				id_next_area_south IS NOT NULL AS south,\
				id_next_area_east IS NOT NULL AS east,\
				id_next_area_west IS NOT NULL AS west\
			FROM\
				area\
			WHERE\
				id_area = ?\
		"

		return Model.fetchOneRow(query, [idArea])


class exception(BaseException):
	pass
