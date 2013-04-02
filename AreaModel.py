# -*- coding: utf8 -*-

from Model import Model


class AreaModel(Model):
	def __init__(self):
		self._areaFields = dict()

	@staticmethod
	def loadByIdCharacterAndDirection(idCharacter, direction):
		if direction not in ('north', 'south', 'east', 'west'):
			raise BaseException('Unknown direction')

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

		model = Model.fetchOneRow(query, [idCharacter])
		if len(model) > 0:
			am = AreaModel()
			am._setPk(model['id_area'])
			am.setIdRegion(model['id_region'])
			am.setIdNextAreaNorth(model['id_next_area_north'])
			am.setIdNextAreaEast(model['id_next_area_east'])
			am.setIdNextAreaSouth(model['id_next_area_south'])
			am.setIdNextAreaWest(model['id_next_area_west'])
			return am

		return None

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

	def getPk(self):
		return self._areaFields["id_area"]

	def _setPk(self, pk):
		self._areaFields["id_area"] = pk

	def setIdRegion(self, region):
		self._areaFields["id_region"] = region

	def setIdNextAreaNorth(self, north):
		self._areaFields["id_next_area_north"] = north

	def setIdNextAreaEast(self, east):
		self._areaFields["id_next_area_east"] = east

	def setIdNextAreaSouth(self, south):
		self._areaFields["id_next_area_south"] = south

	def setIdNextAreaWest(self, west):
		self._areaFields["id_next_area_west"] = west
