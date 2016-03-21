# -*- coding: utf-8 -*-
import unittest

import tests.common
import core
from core.localisation import _
from core import Rpg
import models.settings
import json
import sqlite3


class rpgTests(tests.common.common):
		def test_unknown_world(self):
			rpgEngine = Rpg.Rpg()
			try:
				rpgEngine.init("some/unexisting/world", "uselessLogin")
			except core.exception.exception as e:
				self.assertEquals(e.message, _('ERROR_UNKNOWN_SELECTED_WORLD'))

		def test_invalid_world(self):
			rpgEngine = Rpg.Rpg()
			try:
				rpgEngine.init("tests/invalidDB", "uselessLogin")
			except sqlite3.OperationalError as e:
				self.assertTrue(True)

		def test_invalid_action_format(self):
			rpgEngine = Rpg.Rpg()
			rpgEngine.init(self.dbFile, self.login)
			try:
				rpgEngine.setAction("not list action")
			except TypeError as e:
				self.assertEquals(e.message, _('ERROR_INVALID_FORMAT_ACTION'))

		def test_invalid_action_text(self):
			self.rpgText.setAction(["Unknown action"])
			output = self.rpgText._runAction()
			self.assertEquals(output, _('ERROR_UNKNOWN_COMMAND'))

		def test_invalid_action_json(self):
			self.rpgJSON.setAction(["Unknown action"])
			output = self.rpgJSON._runAction()
			self.assertEquals(output,  {'error': {'message': _('ERROR_UNKNOWN_COMMAND'), 'code': 1}})
