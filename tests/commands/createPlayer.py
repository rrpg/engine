# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from core.localisation import _
import json


class createPlayerTests(tests.common.common):
	login = None
	password = None

	def test_no_argument_provided_text(self):
		self.rpgText.setAction([_('CREATE_PLAYER_COMMAND')])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_SIGNUP_NOT_ENOUGH_ARGUMENTS'))

	def test_no_argument_provided_json(self):
		self.rpgJSON.setAction([_('CREATE_PLAYER_COMMAND')])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_SIGNUP_NOT_ENOUGH_ARGUMENTS'), "code": 1}})

	def test_login_already_used_text(self):
		self.rpgText.setAction([_('CREATE_PLAYER_COMMAND'), 'TEST_PLAYER', 'TEST_PLAYER', 1, 1])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_SIGNUP_LOGIN_ALREADY_USED'))

	def test_login_already_used_json(self):
		self.rpgJSON.setAction([_('CREATE_PLAYER_COMMAND'), 'TEST_PLAYER', 'TEST_PLAYER', 1, 1])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_SIGNUP_LOGIN_ALREADY_USED'), "code": 1}})

	def test_invalid_gender_text(self):
		self.rpgText.setAction([_('CREATE_PLAYER_COMMAND'), 'TEST_PLAYER_SOME', 'TEST_PLAYER', 'some gender', 1])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_SIGNUP_INVALID_GENDER'))

	def test_invalid_gender_json(self):
		self.rpgJSON.setAction([_('CREATE_PLAYER_COMMAND'), 'TEST_PLAYER_SOME', 'TEST_PLAYER', 'some gender', 1])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_SIGNUP_INVALID_GENDER'), "code": 1}})

	def test_invalid_species_text(self):
		self.rpgText.setAction([_('CREATE_PLAYER_COMMAND'), 'TEST_PLAYER_SOME', 'TEST_PLAYER', '1', 'some species'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_SIGNUP_INVALID_SPECIES'))

	def test_invalid_species_json(self):
		self.rpgJSON.setAction([_('CREATE_PLAYER_COMMAND'), 'TEST_PLAYER_SOME', 'TEST_PLAYER', '1', 'some species'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_SIGNUP_INVALID_SPECIES'), "code": 1}})

	def test_text(self):
		self.rpgText.setAction([_('CREATE_PLAYER_COMMAND'), 'TEST_PLAYER_SOME', 'TEST_PLAYER', '1', '1'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('PLAYER_CREATION_CONFIRMATION'))

	def test_json(self):
		self.rpgJSON.setAction([_('CREATE_PLAYER_COMMAND'), 'TEST_PLAYER_SOME', 'TEST_PLAYER', '1', '1'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == ('TEST_PLAYER_SOME', 'TEST_PLAYER'))

unittest.main()
