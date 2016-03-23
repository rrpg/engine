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
	def test_parsed_action(self):
		parsed = Rpg.Rpg.parseTypedAction("some action to parse")
		self.assertEquals(parsed, ["some", "action", "to", "parse"])

	def test_parsed_action_with_single_quotes(self):
		parsed = Rpg.Rpg.parseTypedAction("some action 'to parse'")
		self.assertEquals(parsed, ["some", "action", "to parse"])

	def test_parsed_action_with_double_quotes(self):
		parsed = Rpg.Rpg.parseTypedAction('some action "to parse"')
		self.assertEquals(parsed, ["some", "action", "to parse"])

	def test_parsed_action_with_one_single_quote(self):
		parsed = Rpg.Rpg.parseTypedAction("some action 'to parse")
		self.assertEquals(parsed, ["some", "action", "to parse"])

	def test_parsed_action_with_three_double_quotes(self):
		parsed = Rpg.Rpg.parseTypedAction('some "other action" "to parse')
		self.assertEquals(parsed, ["some", "other action", 'to parse'])

	def test_parsed_action_with_three_single_quotes(self):
		parsed = Rpg.Rpg.parseTypedAction("some 'other action' 'to parse")
		self.assertEquals(parsed, ["some", "other action", "to parse"])

	def test_parsed_action_with_one_double_quote(self):
		parsed = Rpg.Rpg.parseTypedAction('some action "to parse')
		self.assertEquals(parsed, ["some", "action", 'to parse'])

	def test_double_quote_in_action(self):
		parsed = Rpg.Rpg.parseTypedAction('test l"arche')
		self.assertEquals(parsed, ["test", 'l"arche'])

	def test_single_quote_in_action(self):
		parsed = Rpg.Rpg.parseTypedAction("test l'arche")
		self.assertEquals(parsed, ["test", "l'arche"])
