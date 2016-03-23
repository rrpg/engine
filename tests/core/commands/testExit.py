# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json

class exitTests(tests.common.common):
	def test_no_place_given_text(self):
		self.rpgText.setAction([_('EXIT_COMMAND')])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('ERROR_EXIT_NO_PLACE_GIVEN'))

	def test_no_place_given_json(self):
		self.rpgJSON.setAction([_('EXIT_COMMAND')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"error": {"message": _('ERROR_EXIT_NO_PLACE_GIVEN'), "code": 1}})

	def test_place_not_available_text(self):
		self.rpgText.setAction([_('EXIT_COMMAND'), _('PLACE_TYPE_CAVE')])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('ERROR_ENTER_PLACE_NOT_AVAILABLE'))

	def test_place_not_available_json(self):
		self.rpgJSON.setAction([_('EXIT_COMMAND'), _('PLACE_TYPE_CAVE')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"error": {"message": _('ERROR_ENTER_PLACE_NOT_AVAILABLE'), "code": 1}})

	def test_wrong_place_text(self):
		self.rpgText.setAction([_('EXIT_COMMAND'), 'dummyplace'])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('ERROR_UNKNOWN_PLACE_TYPE'))

	def test_wrong_place_given_json(self):
		self.rpgJSON.setAction([_('EXIT_COMMAND'), 'dummyplace'])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"error": {"message": _('ERROR_UNKNOWN_PLACE_TYPE'), "code": 1}})

	def test_when_still_out_text(self):
		self.rpgText.setAction([_('EXIT_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('ERROR_ENTER_PLACE_NOT_AVAILABLE'))

	def test_when_still_out_json(self):
		self.rpgJSON.setAction([_('EXIT_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, {"error": {"message": _('ERROR_ENTER_PLACE_NOT_AVAILABLE'), "code": 1}})

	def test_text(self):
		self.rpgText.setAction([_('ENTER_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		self.rpgText._runAction()
		self.rpgText.setAction([_('EXIT_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('EXIT_CONFIRMATION'))

	def test_json(self):
		self.rpgJSON.setAction([_('ENTER_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		self.rpgJSON._runAction()
		self.rpgJSON.setAction([_('EXIT_COMMAND'), _('PLACE_TYPE_DUNGEON')])
		output = self.rpgJSON._runAction()
		self.assertEquals(output, [_('EXIT_CONFIRMATION')])