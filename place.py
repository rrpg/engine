# -*- coding: utf8 -*-

"""
Module to handle the places types, such as the dungeons.
"""

from Model import Model
import config
import area
import os
import sys


class factory:
	"""
	Class to
	"""

	types = ('dungeon')

	@staticmethod
	def create(idArea, t):
		return factory._get(idArea, t, True)

	@staticmethod
	def get(idArea, t):
		return factory._get(idArea, t, False)

	@staticmethod
	def _get(idArea, t, generate):
		if t not in factory.types:
			raise exception('Unknown place type')

		if t == 'dungeon':
			return dungeon.getAvailable(idArea, generate)


class randomPlace:
	@classmethod
	def getAvailable(cls, idArea, generate):
		"""
		Method to get the informations of a dungeon being in an area.
		If the dungeon is not yet generated, it will be done here.
		"""
		d = model.getOneFromTypeAndArea(cls.areaType, idArea)

		if len(d) == 0:
			raise exception('There is no such place here.')

		if generate and d['entrance_id'] is None:
			cls.generate(d)

		return d

	@classmethod
	def generate(cls, place):
		"""
		Generate a place using an external generating tool

		@param place Place entity representing the place
		"""

		print('Generating place...')
		pipe = os.popen(config.generator['dungeon']['generator'])
		d = pipe.read().strip().split('\n')
		pipe.close()

		# Import an external check class from the generator
		sys.path.insert(0, config.generator['dungeon']['path'])
		import checks

		containerName = cls.areaType + '_' + str(place['id_place'])
		idRegion = area.model.loadById(place['id_area'], ('id_region'))['id_region']

		for index, room in enumerate(d):
			if int(room) == 0:
				continue

			areaId = area.model.insert({
				'id_area_type': place['id_area_type'],
				'x': index % 10,
				'y': index / 10,
				'directions': checks.getDirections(room) >> 2,
				'container': containerName,
				'id_region': idRegion
			})

			if checks.isEntrance(int(room)):
				model.update(
					{'entrance_id': areaId},
					('id_place = ?', [place['id_place']])
				)


class dungeon(randomPlace):
	areaType = 'dungeon'


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
	def getOneFromTypeAndArea(areaType, idArea):
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
				(id_area = ? OR entrance_id = ?)\
				AND at.name = ?\
		"

		return Model.fetchOneRow(query, [idArea, idArea, areaType])


class exception(BaseException):
	"""
	Exception class for the places
	"""
	pass
