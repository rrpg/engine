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
			rpgEngine.initWorld("some/unexisting/world")
			rpgEngine.initPlayer("uselessLogin")
		except core.exception.exception as e:
			self.assertEquals(str(e), _('ERROR_UNKNOWN_SELECTED_WORLD'))

	def test_invalid_world(self):
		rpgEngine = Rpg.Rpg()
		rpgEngine.initWorld("tests/invalidDB")
		self.assertRaises(sqlite3.OperationalError, rpgEngine.initPlayer, "uselessLogin")

	def test_invalid_action_format(self):
		rpgEngine = Rpg.Rpg()
		rpgEngine.initWorld(self.dbFile)
		rpgEngine.initPlayer(self.login)
		with self.assertRaises(TypeError) as raised:
			rpgEngine.setAction("not list action")
		self.assertEquals(str(raised.exception), _('ERROR_INVALID_FORMAT_ACTION'))

	def test_invalid_action_text(self):
		self.rpg.setAction(["Unknown action"])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_UNKNOWN_COMMAND'))

	def test_invalid_action_json(self):
		self.rpg.setAction(["Unknown action"])
		output = self.rpg._runAction(True)
		self.assertEquals(output,  {'error': {'message': _('ERROR_UNKNOWN_COMMAND'), 'code': 1}})
