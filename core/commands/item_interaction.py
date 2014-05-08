# -*- coding: utf-8 -*-
import core.command
from models.item_container import container
from core.localisation import _


class item_interaction(core.command.command):
	def _getArgs(self):
		nbArgs = len(self._args)
		self._args.reverse()

		container = None
		containerIndex = 1
		argsNames = ['containerId', 'container', 'name']
		args = {'name': '', 'container': None, 'containerId': None}

		if nbArgs == 0:
			raise exception(code=exception.CODE_NO_ITEM_GIVEN)

		try:
			quantity = int(self._args[nbArgs - 1])
			self._args.pop()
		except ValueError:
			# 4 arguments have been provided, but the quantity is invalid
			if nbArgs == 4:
				raise exception(code=exception.CODE_INVALID_FORMAT_QUANTITY)
			quantity = 1

		while len(self._args) > 0:
			args[argsNames.pop()] = self._args.pop()

		try:
			if args['containerId'] is not None:
				args['containerId'] = int(args['containerId'])
		except ValueError:
			raise exception(code=exception.CODE_INVALID_CONTAINER_INDEX)

		if args['name'] == '':
			raise exception(code=exception.CODE_NO_ITEM_GIVEN)
		if quantity < 0:
			raise exception(code=exception.CODE_INVALID_QUANTITY)

		return (quantity, args['name'], args['container'], args['containerId'])

	def _getContainerFromIdAreaTypeAndIndex(self, idArea, containerType, index):
		containers = container.getAllFromIdAreaAndType(idArea, containerType)
		nbContainers = len(containers)

		if nbContainers == 0:
			raise core.command.exception(_('ERROR_CONTAINER_NOT_AVAILABLE'))

		if index is not None:
			index = int(index) - 1

			if index < 0 or index >= nbContainers:
				raise core.command.exception(_('ERROR_OUT_OF_RANGE_ITEM_CONTAINER_INDEX'))

		if nbContainers > 1 and index is None:
			raise core.command.exception(_('ERROR_MULTIPLE_CONTAINERS_AVAILABLE'))

		return containers[index or 0]

class exception(core.exception.exception):
	CODE_NO_ITEM_GIVEN = 1
	CODE_INVALID_QUANTITY = 2
	CODE_INVALID_FORMAT_QUANTITY = 3
	CODE_INVALID_CONTAINER_INDEX = 4

	def getCodes(self):
		return (
			self.CODE_NO_ITEM_GIVEN,
			self.CODE_INVALID_QUANTITY,
			self.CODE_INVALID_FORMAT_QUANTITY,
			self.CODE_INVALID_CONTAINER_INDEX
		)
