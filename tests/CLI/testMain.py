# -*- coding: utf-8 -*-
import unittest

import tests.common
import core
from core.localisation import _
from CLI import main
import models.settings
import json
import sqlite3


class rpgTests(tests.common.common):
	def test_parsed_action(self):
		parsed = main.main.parseTypedAction("some action to parse")
		self.assertEquals(parsed, ["some", "action", "to", "parse"])

	def test_parsed_action_with_single_quotes(self):
		parsed = main.main.parseTypedAction("some action 'to parse'")
		self.assertEquals(parsed, ["some", "action", "to parse"])

	def test_parsed_action_with_double_quotes(self):
		parsed = main.main.parseTypedAction('some action "to parse"')
		self.assertEquals(parsed, ["some", "action", "to parse"])

	def test_parsed_action_with_one_single_quote(self):
		parsed = main.main.parseTypedAction("some action 'to parse")
		self.assertEquals(parsed, ["some", "action", "to parse"])

	def test_parsed_action_with_three_double_quotes(self):
		parsed = main.main.parseTypedAction('some "other action" "to parse')
		self.assertEquals(parsed, ["some", "other action", 'to parse'])

	def test_parsed_action_with_three_single_quotes(self):
		parsed = main.main.parseTypedAction("some 'other action' 'to parse")
		self.assertEquals(parsed, ["some", "other action", "to parse"])

	def test_parsed_action_with_one_double_quote(self):
		parsed = main.main.parseTypedAction('some action "to parse')
		self.assertEquals(parsed, ["some", "action", 'to parse'])

	def test_double_quote_in_action(self):
		parsed = main.main.parseTypedAction('test l"arche')
		self.assertEquals(parsed, ["test", 'l"arche'])

	def test_single_quote_in_action(self):
		parsed = main.main.parseTypedAction("test l'arche")
		self.assertEquals(parsed, ["test", "l'arche"])
