# -*- coding: utf-8 -*-

from models import item, area
import core.command
from core.localisation import _


class item_interaction(core.command.command):
	def _getArgs(self):
		nbArgs = len(self._args)
		self._args.reverse()

		container = None
		containerIndex = 1
		argsNames = ['containerId', 'container', 'name']
		args = {'name': '', 'container': None, 'containerId': 1}

		if nbArgs == 0:
			raise exception(code=exception.CODE_NO_ITEM_GIVEN)

		try:
			quantity = int(self._args[nbArgs - 1])
			self._args.pop()
		except ValueError:
			# 4 arguments have been provided, but the quantity is invalid
			if nbArgs == 4:
				raise exception(code=exception.CODE_INVALID_QUANTITY)
			quantity = 1

		while len(self._args) > 0:
			args[argsNames.pop()] = self._args.pop()

		return (quantity, args['name'], args['container'], args['containerId'])


class exception(core.exception.exception):
	CODE_NO_ITEM_GIVEN = 1
	CODE_INVALID_QUANTITY = 2

	def getCodes(self):
		return (self.CODE_NO_ITEM_GIVEN, self.CODE_INVALID_QUANTITY)
