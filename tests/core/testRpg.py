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
			self.assertEquals(str(e), _('ERROR_UNKNOWN_SELECTED_WORLD'))

	def test_invalid_world(self):
		rpgEngine = Rpg.Rpg()
		self.assertRaises(sqlite3.OperationalError, rpgEngine.init, "tests/invalidDB", "uselessLogin")

	def test_invalid_action_format(self):
		rpgEngine = Rpg.Rpg()
		rpgEngine.init(self.dbFile, self.login)
		with self.assertRaises(TypeError) as raised:
			rpgEngine.setAction("not list action")
		self.assertEquals(str(raised.exception), _('ERROR_INVALID_FORMAT_ACTION'))

	def test_invalid_action_text(self):
		self.rpgText.setAction(["Unknown action"])
		output = self.rpgText._runAction()
		self.assertEquals(output, _('ERROR_UNKNOWN_COMMAND'))

	def test_invalid_action_json(self):
		self.rpgJSON.setAction(["Unknown action"])
		output = self.rpgJSON._runAction()
		self.assertEquals(output,  {'error': {'message': _('ERROR_UNKNOWN_COMMAND'), 'code': 1}})

	def test_parsed_action(self):
		rpgEngine = Rpg.Rpg()
		parsed = rpgEngine.parseTypedAction("some action to parse")
		self.assertEquals(parsed, ["some", "action", "to", "parse"])

	def test_parsed_action_with_single_quotes(self):
		rpgEngine = Rpg.Rpg()
		parsed = rpgEngine.parseTypedAction("some action 'to parse'")
		self.assertEquals(parsed, ["some", "action", "to parse"])

	def test_parsed_action_with_double_quotes(self):
		rpgEngine = Rpg.Rpg()
		parsed = rpgEngine.parseTypedAction('some action "to parse"')
		self.assertEquals(parsed, ["some", "action", "to parse"])

	def test_parsed_action_with_one_single_quote(self):
		rpgEngine = Rpg.Rpg()
		parsed = rpgEngine.parseTypedAction("some action 'to parse")
		self.assertEquals(parsed, ["some", "action", "to parse"])

	def test_parsed_action_with_three_double_quotes(self):
		rpgEngine = Rpg.Rpg()
		parsed = rpgEngine.parseTypedAction('some "other action" "to parse')
		self.assertEquals(parsed, ["some", "other action", 'to parse'])

	def test_parsed_action_with_three_single_quotes(self):
		rpgEngine = Rpg.Rpg()
		parsed = rpgEngine.parseTypedAction("some 'other action' 'to parse")
		self.assertEquals(parsed, ["some", "other action", "to parse"])

	def test_parsed_action_with_one_double_quote(self):
		rpgEngine = Rpg.Rpg()
		parsed = rpgEngine.parseTypedAction('some action "to parse')
		self.assertEquals(parsed, ["some", "action", 'to parse'])

	def test_double_quote_in_action(self):
		rpgEngine = Rpg.Rpg()
		parsed = rpgEngine.parseTypedAction('test l"arche')
		self.assertEquals(parsed, ["test", 'l"arche'])

	def test_single_quote_in_action(self):
		rpgEngine = Rpg.Rpg()
		parsed = rpgEngine.parseTypedAction("test l'arche")
		self.assertEquals(parsed, ["test", "l'arche"])
