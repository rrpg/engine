# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json


class enterTests(tests.common.common):
	def test_empty_text(self):
		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('INVENTORY_EMPTY'))

	def test_empty_json(self):
		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, [])

	def test_not_empty_text(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		output = self.rpg._runAction()
		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction()
		self.assertEquals(output, '  2 Heavy breastplate')

	def test_not_empty_json(self):
		self.rpg.setAction([_('TAKE_COMMAND'), 2, 'Heavy breastplate'])
		output = self.rpg._runAction(True)
		self.rpg.setAction([_('INVENTORY_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, [{"name": "Heavy breastplate", "quantity": 2}])
