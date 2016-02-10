# -*- coding: utf-8 -*-
import unittest
import sys
import os
sys.path.append(os.path.realpath(__file__ + "/../../../"))

import tests.common
from core.localisation import _
import json


class authenticateTest(tests.common.common):
	login = None

	def test_not_enough_argument_provided_text(self):
		self.rpgText.setAction(['authenticate'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_AUTHENTICATE_ARGUMENTS_NUMBER'))

	def test_not_enough_provided_json(self):
		self.rpgJSON.setAction(['authenticate'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_AUTHENTICATE_ARGUMENTS_NUMBER'), "code": 1}})

	def test_invalid_credentials_text(self):
		self.rpgText.setAction(['authenticate', 'bad-login'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('ERROR_CONNECT_INVALID_CREDENTIALS'))

	def test_invalid_credentials_json(self):
		self.rpgJSON.setAction(['authenticate', 'bad-login'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == {"error": {"message": _('ERROR_CONNECT_INVALID_CREDENTIALS'), "code": 1}})

	def test_ok_text(self):
		self.rpgText.setAction(['authenticate', 'TEST_PLAYER'])
		output = self.rpgText._runAction()
		self.assertTrue(output == _('PLAYER_AUTHENTICATION_CONFIRMATION'))

	def test_ok_json(self):
		self.rpgJSON.setAction(['authenticate', 'TEST_PLAYER'])
		output = self.rpgJSON._runAction()
		self.assertTrue(output == [True])
