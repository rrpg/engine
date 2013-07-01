# -*- coding: utf8 -*-

"""
Module to handle the areas in the game.
The world is divided in a grid of areas.
An area can have up to 4 neighbours (one for each cardinal point).
"""

from Model import Model

import json

"""
Available directions
"""
directions = ['north', 'south', 'east', 'west']


class area:
	"""
	Class to interact with the areas in the game.
	"""

	"""
	Available items of the area.

	@param dict
	"""
	items = dict()

	@staticmethod
	def getNeighbourgFromDirection(idArea, direction):
		"""
		area.area.getNeighbourgFromDirection(idArea, direction) -> area.area

		Return the neighbourg area of the given area according to the given
		direction.

		@param idArea integer id of the reference area
		@param direction string direction of the area to return, must be in
			area.directions.

		@return area.area if an area is found, None else.
		"""
		m = model.getNeighbourgFromDirection(idArea, direction)

		if len(m) == 0:
			return None
		else:
			a = area()
			a._model = m
			return a

	@staticmethod
	def getItems(idArea):
		"""
		area.area.getItems(idArea) -> list()

		Method to get the items available in an area.

		@param idArea id of the desired area.

		@return list
		"""
		if idArea not in area.items.keys():
			area.items[idArea] = json.loads(model.loadById(idArea, ['items'])['items'])
		return area.items[idArea]

	@staticmethod
	def removeItems(idArea, items):
		"""
		area.area.removeItems(idArea, items)

		Method to remove some items in an area.
		Items not in the area will be ignored.

		@param idArea id of the area the items must be removed from.
		@param items list of items to remove
		"""
		area.items[idArea] = filter(lambda k: k not in items, area.getItems(idArea))
		model.saveAvailableItems(idArea, area.items[idArea])

	@staticmethod
	def addItems(idArea, items):
		area.items[idArea] = area.getItems(idArea) + items
		model.saveAvailableItems(idArea, area.items[idArea])


class model(Model):
	"""
	Class to interact with the values in the database.
	"""

	fields = [
		'id_area', 'id_region',
		'id_next_area_north', 'id_next_area_east', 'id_next_area_south', 'id_next_area_west',
		'items'
	]

	@staticmethod
	def getNeighbourgFromDirection(idArea, direction):
		"""
		area.model.getNeighbourgFromDirection(idArea, direction) -> dict()

		Returns the neighbourg of the area given in arguments from a given
		direction.

		@param idArea integer id of the reference area
		@direction string direction (from the reference area) of the area to
		return, must be a value of area.directions.

		@return dict informations of the found area, empty dict if not found.
		"""
		if direction not in (directions):
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
			WHERE\
				ap.id_area = ?\
		" % direction

		return Model.fetchOneRow(query, [idArea])

	@staticmethod
	def getSurroundingAreas(idArea):
		"""
		area.getSurroundingAreas(idArea) -> dict()

		Return the available neighbourg areas of the area given in argument.

		@param idArea integer id of the reference area

		@return dict a list of directions, with for each direction, True if
			there is an area in this direction, False else.
		"""
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

	@staticmethod
	def saveAvailableItems(idArea, items):
		"""
		area.model.saveAvailableItems(idArea, items)

		Update an area's items list.

		@param idArea id of the area the items must be removed from.
		@param items list of items to remove
		"""
		model.update(
			{'items': json.dumps(items)},
			('id_area = ?', [idArea])
		)

class exception(BaseException):
	"""
	Class for the exceptions concerning areas.
	"""
	pass
