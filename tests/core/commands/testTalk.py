# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json


class talkTests(tests.common.common):
	def test_no_character_given_text(self):
		self.rpg.setAction([_('TALK_COMMAND')])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_TALK_NO_CHARACTER_GIVEN'))

	def test_no_character_given_json(self):
		self.rpg.setAction([_('TALK_COMMAND')])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TALK_NO_CHARACTER_GIVEN'), "code": 1}})

	def test_no_sentence_given_text(self):
		self.rpg.setAction([_('TALK_COMMAND'), 'Someone'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_TALK_NO_SENTENCE_GIVEN'))

	def test_no_sentence_given_json(self):
		self.rpg.setAction([_('TALK_COMMAND'), 'Someone'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TALK_NO_SENTENCE_GIVEN'), "code": 1}})

	def test_unknown_character_text(self):
		self.rpg.setAction([_('TALK_COMMAND'), 'Someone', 'Something'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TALK_UNKNOWN_CHARACTER'), "code": 1}})

	def test_unknown_character_json(self):
		self.rpg.setAction([_('TALK_COMMAND'), 'Someone', 'Something'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TALK_UNKNOWN_CHARACTER'), "code": 1}})

	def test_unknown_sentence_text(self):
		self.rpg.setAction([_('TALK_COMMAND'), 'Tom', 'Something'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_TALK_UNKNOWN_SENTENCE'), "code": 1}})

	def test_text(self):
		self.rpg.setAction([_('TALK_COMMAND'), 'Tom', 'hi'])
		output = self.rpg._runAction()
		self.assertTrue(output in ["Hi, my name is Tom, I'm a butcher", "Hi, TEST_PLAYER"])

	def test_json(self):
		self.rpg.setAction([_('TALK_COMMAND'), 'Tom', 'hi'])
		output = self.rpg._runAction(True)
		self.assertTrue(
			output == {"question": "hi", "character": "Tom", "answer": "Hi, my name is Tom, I'm a butcher"}
			or output == {"question": "hi", "character": "Tom", "answer": "Hi, TEST_PLAYER"}
		)
