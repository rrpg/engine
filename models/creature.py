# -*- coding: utf-8 -*-

"""
Module to handle the enemies to fight
"""

from models.Model import Model


class creature:
	"""
	Class to interact with the creatures in the game.
	"""

	@staticmethod
	def getFromAreaType(idAreaType, probability):
		if probability == 0.000:
			return None

		c = model.getFromAreaType(idAreaType, probability)
		if c == {}:
			return None

		return c


class model(Model):
	"""
	Class to interact with the values in the database.
	"""

	fields = (
		'id_creature', 'name'
	)

	@staticmethod
	def getFromAreaType(idAreaType, probability):
		"""
		emeny.model.getFromArea(area) -> dict()

		Return a random enemy that the player can encounter in a given
		area type

		@param idAreaType dict area where the enemy can be found
		@param probability float the probability of finding an enemy

		@return dict an enemy or None if no enemy can be found in the
		given area type
		"""
		query = "\
			SELECT\
				name,\
				stats_hp,\
				stat_strength,\
				stat_defence,\
				stat_speed,\
				stat_accuracy\
			FROM\
				creature\
				JOIN creature_area_type ON creature.id_creature = creature_area_type.id_creature\
			WHERE\
				creature_area_type.id_area_type = ?\
				AND creature_area_type.probability >= ?\
			ORDER BY RANDOM() LIMIT 1\
		"

		return Model.fetchOneRow(query, [idAreaType, probability])
