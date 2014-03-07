# -*- coding: utf-8 -*-

"""
Module to handle the places types, such as the dungeons.
"""

from Model import Model
import config
import area
import subprocess
import sys
from localisation import _

types = (_('PLACE_TYPE_DUNGEON'), _('PLACE_TYPE_CAVE'))

class factory:
	"""
	Class to load places from a given type
	"""

	@staticmethod
	def getFromExitArea(idArea, t):
		if t not in types:
			raise exception(_('ERROR_UNKNOWN_PLACE_TYPE'))

		if t == _('PLACE_TYPE_DUNGEON'):
			return dungeon.getAvailableFromExitArea(idArea)
		if t == _('PLACE_TYPE_CAVE'):
			return cave.getAvailableFromExitArea(idArea)

	@staticmethod
	def getFromEntranceArea(idArea, t):
		if t not in types:
			raise exception(_('ERROR_UNKNOWN_PLACE_TYPE'))

		if t == _('PLACE_TYPE_DUNGEON'):
			return dungeon.getAvailable(idArea)
		elif t == _('PLACE_TYPE_CAVE'):
			return cave.getAvailable(idArea)

	@staticmethod
	def generate(place, t):
		if t not in types:
			raise exception(_('ERROR_UNKNOWN_PLACE_TYPE'))

		if t == _('PLACE_TYPE_DUNGEON'):
			return dungeon.generate(place)
		elif t == _('PLACE_TYPE_CAVE'):
			return cave.generate(place)


class randomPlace:
	@classmethod
	def getAvailable(cls, idArea):
		"""
		Method to get the informations of a dungeon being in an area.
		"""
		p = model.getOneFromTypeAndEntranceId(cls.areaType, idArea)
		if len(p) == 0:
			return None

		return p

	@classmethod
	def getAvailableFromExitArea(cls, idArea):
		"""
		Method to get the informations of a place from the area if its exit
		cell.
		"""
		d = model.getOneFromTypeAndExitId(cls.areaType, idArea)

		if len(d) == 0:
			return None

		return d

	@classmethod
	def generate(cls, place):
		"""
		Generate a place using an external generating tool

		@param place Place entity representing the place
		"""

		print(_('GENERATING_WAITING_TEXT'))
		p = subprocess.Popen(
			config.generator['dungeon']['generator'],
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)

		result = p.communicate()

		if result[1] is not '':
			raise exception(_('ERROR_PLACE_GENERATION'))
		d = result[0].strip().split('\n')

		# Import an external check class from the generator
		sys.path.insert(0, config.generator['dungeon']['path'])
		import checks

		containerName = cls.areaType + '_' + str(place['id_place'])
		idRegion = area.model.loadById(place['id_area'], ('id_region'))['id_region']

		Model.connect()
		c = Model.getCursor()
		query = "INSERT INTO area\
			(id_area_type, x, y, directions, container, id_region)\
			VALUES (:id_area_type, :x, :y, :directions, :container, :id_region)"
		for index, room in enumerate(d):
			if int(room) == 0:
				continue

			params = {
				'id_area_type': place['id_area_type'],
				'x': index % 10,
				'y': index / 10,
				'directions': checks.getDirections(room) >> 2,
				'container': containerName,
				'id_region': idRegion
			}
			Model.executeQuery(c, query, params)

			if checks.isEntrance(int(room)):
				entrance = c.lastrowid
		Model.disconnect()

		model.update(
			{'entrance_id': entrance},
			('id_place = ?', [place['id_place']])
		)
		place['entrance_id'] = entrance
		return place


class dungeon(randomPlace):
	areaType = _('PLACE_TYPE_DUNGEON')


class cave(randomPlace):
	areaType = _('PLACE_TYPE_CAVE')


class model(Model):

	fields = ('id_place', 'id_area_type', 'id_area', 'name', 'entrance_id')

	@staticmethod
	def getSurroundingPlaces(idArea):
		"""
		place.model.getSurroundingPlaces(idArea) -> dict()

		Return the places being in the area given in argument.

		@param idArea integer id of the reference area

		@return list a list of places
		"""
		query = "\
			SELECT\
				CASE WHEN id_area = ? THEN p.name ELSE 'Exit of ' || p.name END AS name\
			FROM\
				place AS p\
				JOIN area_type AS at ON p.id_area_type = at.id_area_type\
			WHERE\
				id_area = ?\
				OR entrance_id = ?\
		"

		return Model.fetchAllRows(query, [idArea, idArea, idArea])

	@staticmethod
	def getOneFromTypeAndEntranceId(areaType, idArea):
		"""
		Method to get the informations of a place in a given area
		"""

		query = "\
			SELECT\
				*\
			FROM\
				place AS p\
				JOIN area_type AS at ON p.id_area_type = at.id_area_type\
			WHERE\
				id_area = ?\
				AND at.name = ?\
		"

		return Model.fetchOneRow(query, [idArea, areaType])

	@staticmethod
	def getOneFromTypeAndExitId(areaType, idArea):
		"""
		Method to get the informations of a place in a given area
		"""

		query = "\
			SELECT\
				*\
			FROM\
				place AS p\
				JOIN area_type AS at ON p.id_area_type = at.id_area_type\
			WHERE\
				entrance_id = ?\
				AND at.name = ?\
		"

		return Model.fetchOneRow(query, [idArea, areaType])


class exception(BaseException):
	"""
	Exception class for the places
	"""
	pass
