# -*- coding: utf-8 -*-

"""
Module to handle the areas in the game.
The world is divided in a grid of areas.
An area can have up to 4 neighbours (one for each cardinal point).
"""

from Model import Model
import item

import json
from localisation import _

"""
Available directions
"""
directions = {
	_('DIRECTION_KEY_NORTH'): (1, (0, -1)),
	_('DIRECTION_KEY_EAST'): (2, (1, 0)),
	_('DIRECTION_KEY_SOUTH'): (4, (0, 1)),
	_('DIRECTION_KEY_WEST'): (8, (-1, 0))
}


class area:
	"""
	Class to interact with the areas in the game.
	"""

	"""
	Available items of the area.

	@param dict
	"""
	items = dict()
	types = (_('AREA_TYPE_LAND'), _('AREA_TYPE_DUNGEON'))

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
		a = model.loadById(idArea)
		m = model.getFromDirection(
			(a['x'] + directions[direction][1][0], a['y'] + directions[direction][1][1])
		)

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
			area.items[idArea] = item.inventory.fromStr(model.loadById(idArea, ['items'])['items'])
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
		area.items[idArea] = item.inventory.removeItems(area.getItems(idArea), items)
		model.saveAvailableItems(idArea, area.items[idArea])

	@staticmethod
	def addItems(idArea, items):
		"""
		area.area.addItems(idArea, items)

		Method to add some items in an area.

		@param idArea id of the area the items must be added to.
		@param items list of items to add
		"""
		area.items[idArea] = item.inventory.addItems(area.getItems(idArea), items)
		model.saveAvailableItems(idArea, area.items[idArea])

	@staticmethod
	def getDirections():
		"""
		Return the list of possible directions
		"""

		return directions.keys()

	@staticmethod
	def getValidDirections(directionsBits):
		"""
		From a integer containing, for each bits, a direction, a list will
		be returned containing the directions being in the integer.
		For example, if directionBits == 6 (0b0110), the returned directions
		will be ("east", "south").
		Uses the package variable directions.
		"""
		return filter(lambda k: area.canGoTo(directionsBits, k), directions)

	@staticmethod
	def canGoTo(directionsBits, direction):
		"""
		Check if a direction match a provided integer.
		For example, if directionBits == 6 (0b0110), the method will return true
		if direction == "east" or "south".
		Uses the package variable directions.
		"""
		return (directions[direction][0] & directionsBits) == directions[direction][0]

	@staticmethod
	def getRegionNameFromAreaId(idArea):
		return model.getRegionNameFromAreaId(idArea)

class model(Model):
	"""
	Class to interact with the values in the database.
	"""

	fields = (
		'id_area', 'id_region',
		'x', 'y',
		'directions',
		'container',
		'items'
	)

	@staticmethod
	def getRegionNameFromAreaId(idArea):
		"""
		area.model.getRegionNameFromAreaId(idArea) -> string

		Returns the name of the current area's region.

		@param idArea integer id of the reference area

		@return string name of the region
		"""

		query = "\
			SELECT\
				r.region_name\
			FROM\
				area AS a\
				JOIN region AS r\
			WHERE\
				a.id_area = ?\
		"

		return Model.fetchOneRow(query, [idArea])['region_name']

	@staticmethod
	def getFromDirection(direction):
		"""
		area.model.getFromDirection(direction) -> dict()

		Returns the neighbourg of the area given in arguments from a given
		direction.

		@direction tuple of the area to return, represented by its relative
			values of x and y from idArea ((-1, 0) for example)

		@return dict informations of the found area, empty dict if not found.
		"""

		query = "\
			SELECT\
				%s\
			FROM\
				area\
			WHERE\
				x = ?\
				AND y = ?\
		" % (', '.join(model.fields))

		return Model.fetchOneRow(query, direction)

	@staticmethod
	def getSurroundingAreas(idArea):
		"""
		area.model.getSurroundingAreas(idArea) -> dict()

		Return the available neighbourg areas of the area given in argument.

		@param idArea integer id of the reference area

		@return dict a list of directions, with for each direction, True if
			there is an area in this direction, False else.
		"""
		query = "\
			SELECT\
				orig.directions\
			FROM\
				area AS orig\
				JOIN area AS dest ON (dest.x = orig.x - 1 OR dest.x = orig.x + 1 OR dest.x = orig.x)\
					AND (dest.y = orig.y - 1 OR dest.y = orig.y + 1 OR dest.y = orig.y)\
					AND orig.id_area <> dest.id_area\
			WHERE\
				orig.id_area = ?\
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
