# -*- coding: utf8 -*-

"""
Module to handle the areas in the game.
The world is divided in a grid of areas.
An area can have up to 4 neighbours (one for each cardinal point).
"""

from Model import Model
import item

import json

"""
Available directions
"""
directions = {'north': (0, -1), 'south': (0, 1), 'east': (-1, 0), 'west': (1, 0)}


class area:
	"""
	Class to interact with the areas in the game.
	"""

	"""
	Available items of the area.

	@param dict
	"""
	items = dict()
	types = ('land', 'dungeon')

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
			(a['x'] + directions[direction][0], a['y'] + directions[direction][1])
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


class model(Model):
	"""
	Class to interact with the values in the database.
	"""

	fields = (
		'id_area', 'id_region',
		'x', 'y',
		'items'
	)

	@staticmethod
	def getFromDirection(direction):
		"""
		area.model.getFromDirection(idArea, direction) -> dict()

		Returns the neighbourg of the area given in arguments from a given
		direction.

		@param idArea integer id of the reference area
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
				CASE WHEN dest.x = orig.x - 1 THEN dest.id_area ELSE NULL END AS west,\
				CASE WHEN dest.x = orig.x + 1 THEN dest.id_area ELSE NULL END AS east,\
				CASE WHEN dest.y = orig.y - 1 THEN dest.id_area ELSE NULL END AS north,\
				CASE WHEN dest.y = orig.y + 1 THEN dest.id_area ELSE NULL END AS south\
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
