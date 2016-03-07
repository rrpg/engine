# -*- coding: utf-8 -*-

"""
Module to handle the characters in the game
"""

from models.Model import Model
from models import item
import core.exception


class character:
	"""
	Class to interact with the characters in the game.
	"""

	inventory = None
	_isFighting = False

	@staticmethod
	def searchByNameAndIdArea(name, idArea):
		"""
		character.character.searchByNameAndIdArea(name, idArea) -> character.character

		Search a character from its name in a given area

		@param name string name of the character to search
		@param idArea integer id of the area where the character is searched

		@return character.character if found, else None
		"""
		m = model.loadBy({'name': name, 'id_area': idArea})
		if len(m) > 0:
			return character.loadFromModel(m[0])
		return None

	@staticmethod
	def searchByIdArea(idArea):
		"""
		character.character.searchByIdArea(idArea) -> list

		Search characters being in an area which id is given in argument.

		@param idArea integer id of the area where the characters are searched

		@return list list of characters founds
		"""
		models = model.loadBy({'id_area': idArea})
		chars = list()
		for m in models:
			chars.append(character.loadFromModel(m))
		return chars

	@staticmethod
	def loadFromModel(m):
		"""
		character.character.loadFromModel(m) -> character.character

		Create a character from a given model.

		@param m dict model of the character to create

		@return character.character if the model is not empty, else None
		"""
		if len(m) == 0:
			return None
		else:
			c = character()
			c._model = m
			return c

	def getId(self):
		"""
		c.getId() -> integer

		Returns the character's id

		@return integer character's id
		"""
		return self._model['id_character']

	def canFight(self):
		"""
		c.canFight() -> boolean

		Returns true if the character can fight

		@return boolean
		"""
		return self._model['can_fight']

	def isFighting(self):
		"""
		c.isFighting() -> boolean

		Returns true if the character is fighting

		@return boolean
		"""
		return self._isFighting

	def fight(self, value):
		"""
		c.fight(Bool)

		Set the attribute isFighting to true or false
		"""
		self._isFighting = value

	def getStats(self):
		"""
		c.getStats() -> dict

		Return a dict with the characters stats. the keys are the stats names,
		taken from the model's field names, minus the stats_prefix

		@return dict
		"""
		return {name: self._model[name] for name in self._model.keys() if name[:5] == 'stat_'}

	def goTo(self, idArea):
		"""
		character.character.goTo(idArea)

		Move a character to a given area

		@param idArea id of the area where the character must go.
		"""
		self._model['id_area'] = idArea
		model.savePosition(self._model['id_character'], self._model['id_area'])

	def getInventory(self):
		"""
		character.character.getInventory() -> dict()

		Returns the character's items.
		The inventory has the following format:
		{
			idItem: {'quantity': number}
		}

		@return dict the character's inventory
		"""
		if self.inventory is None:
			self.inventory = item.inventory.fromStr(str(self._model['inventory']))
		return self.inventory

	def addItemsToInventory(self, itemsId):
		"""
		character.character.addItemsToInventory(itemsIds)

		Add a list of items in the character's inventory.

		@param itemsId ids of the items to add
		"""
		self.inventory = item.inventory.addItems(self.getInventory(), itemsId)
		model.saveInventory(self._model['id_character'], self.inventory)

	def removeItemsFromInventory(self, itemsId):
		"""
		character.character.removeItemsFromInventory(itemsIds)

		Remove a list of items from the character's inventory.

		@param itemsId ids of the items to remove
		"""
		self.inventory = item.inventory.removeItems(self.getInventory(), itemsId)
		model.saveInventory(self._model['id_character'], self.inventory)

	def getAreaId(self):
		"""
		Return the id of the area where the character is
		"""
		return self._model['id_area']

class stats:
	MAX_VALUE = 255

class model(Model):
	"""
	Class to interact with the values in the database.
	"""

	fields = (
		'id_character',
		'name', 'can_fight',
		'stat_current_hp', 'stat_max_hp',
		'stat_strength',
		'stat_defence',
		'stat_speed',
		'stat_accuracy',
		'stat_luck',
		'id_species', 'id_gender', 'id_area', 'inventory')

	@staticmethod
	def savePosition(idCharacter, idArea):
		"""
		character.model.savePosition(idCharacter, idArea)

		Change a character's position

		@param idCharacter integer id of the character to move
		@param idArea id of the area where the character must go.
		"""
		model.update(
			{'id_area': idArea},
			('id_character = ?', [idCharacter])
		)

	@staticmethod
	def saveInventory(idCharacter, inventory):
		"""
		character.model.saveInventory(idCharacter, inventory)

		Save the character's inventory in the database.

		@param idCharacter character's id.
		@param inventory list items to add.
		"""
		model.update(
			{'inventory': item.inventory.toStr(inventory)},
			('id_character = ?', [idCharacter])
		)


class exception(core.exception.exception):
	"""
	Class for the exceptions concerning characters.
	"""
	pass
