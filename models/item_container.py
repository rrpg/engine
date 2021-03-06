# -*- coding: utf-8 -*-

from models.Model import Model
from models import item
from core.localisation import _
import core.exception
from core import config
import json

class container:
	"""
	Class to interact with the item containers, such as chests.
	"""

	containersToSave = dict()

	@staticmethod
	def getMemoizedItems(c):
		idContainer = c['id_item_container']
		if idContainer in container.containersToSave.keys():
			c['items'] = container.containersToSave[idContainer]
		return c

	@staticmethod
	def getAllFromIdArea(idArea):
		itemContainerTypes = model.getTypes()
		containers = model.loadBy({'id_area': idArea})
		for k, c in enumerate(containers):
			containers[k]['type_label'] = itemContainerTypes[containers[k]['id_item_container_type']]
			containers[k] = container.getMemoizedItems(containers[k])
		return containers

	@staticmethod
	def getAllFromIdAreaAndType(idArea, containerType):
		itemContainerTypes = model.getTypes()
		containerTypeId = None
		for k in itemContainerTypes:
			if itemContainerTypes[k] == containerType:
				containerTypeId = k
				break

		if containerTypeId is None:
			raise exception(_('ERROR_UNKNOWN_ITEM_CONTAINER_TYPE_LABEL'))

		containers = model.loadBy({
			'id_area': idArea,
			'id_item_container_type': containerTypeId
		})

		for k, c in enumerate(containers):
			containers[k] = container.getMemoizedItems(containers[k])

		return containers

	@staticmethod
	def addItems(c, items):
		"""
		item_container.container.addItems(c, items)

		Method to add some items in a container.

		@param container container where the items must be added.
		@param items list of items to add
		"""
		container.containersToSave[c['id_item_container']] = item.inventory.addItems(
			item.inventory.fromStr(c['items']),
			items
		)

	@staticmethod
	def removeItems(c, items):
		"""
		item_container.container.removeItems(c, items)

		Method to remove some items from a container.
		Items not in the container will be ignored.

		@param container container the items must be removed from.
		@param items list of items to remove
		"""
		container.containersToSave[c['id_item_container']] = item.inventory.removeItems(
			item.inventory.fromStr(c['items']),
			items
		)

	@classmethod
	def saveChangedContainers(cls):
		for idContainers in cls.containersToSave:
			model.saveAvailableItems(
				idContainers, cls.containersToSave[idContainers]
			)

		cls.containersToSave = dict()

	@classmethod
	def resetChangedContainers(cls):
		cls.containersToSave = dict()


class model(Model):
	"""
	Class to interact with the values in the database.
	"""

	fields = (
		'id_item_container',
		'id_item_container_type',
		'id_area',
		'items'
	)

	@staticmethod
	def getTypes():
		"""
		Returns the available types as an dict with ids as keys and labels as
		values

		@return dict the types
		"""

		query = "\
			SELECT\
				id_item_container_type,\
				label\
			FROM\
				item_container_type\
		"

		return {t['id_item_container_type']: t['label'] for t in Model.fetchAllRows(query)}

	@staticmethod
	def saveAvailableItems(idContainer, items):
		model.update(
			{'items': json.dumps(items)},
			('id_item_container = ?', [idContainer])
		)


class exception(core.exception.exception):
	"""
	Class for the exceptions concerning item containers.
	"""
	pass
