# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json


class authenticateTest(tests.common.common):
	initPlayer = False

	def test_not_enough_argument_provided_text(self):
		self.rpg.setAction(['authenticate'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_AUTHENTICATE_ARGUMENTS_NUMBER'))

	def test_not_enough_provided_json(self):
		self.rpg.setAction(['authenticate'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_AUTHENTICATE_ARGUMENTS_NUMBER'), "code": 1}})

	def test_invalid_credentials_text(self):
		self.rpg.setAction(['authenticate', 'bad-login'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_CONNECT_INVALID_CREDENTIALS'))

	def test_invalid_credentials_json(self):
		self.rpg.setAction(['authenticate', 'bad-login'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_CONNECT_INVALID_CREDENTIALS'), "code": 1}})

	def test_ok_text(self):
		self.rpg.setAction(['authenticate', 'TEST_PLAYER'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('PLAYER_AUTHENTICATION_CONFIRMATION'))

	def test_ok_json(self):
		self.rpg.setAction(['authenticate', 'TEST_PLAYER'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, [True])
