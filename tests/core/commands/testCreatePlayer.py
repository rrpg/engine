# -*- coding: utf-8 -*-
import unittest

import tests.common
from core.localisation import _
import json
from models.saved_game import saved_game


class createPlayerTests(tests.common.common):
	initPlayer = False

	def compareSavedGamesSaveOk(self):
		saves = saved_game.loadAll()
		expectedSaves = [
			{'id_saved_game': 1, 'login': 'TEST_PLAYER_SOME'},
			{'id_saved_game': 2, 'login': None},
			{'id_saved_game': 3, 'login': None}
		]
		self.assertEquals(saves, expectedSaves)

	def compareSavedGamesSaveKo(self):
		saves = saved_game.loadAll()
		expectedSaves = [
			{'id_saved_game': 1, 'login': 'TEST_PLAYER'},
			{'id_saved_game': 2, 'login': None},
			{'id_saved_game': 3, 'login': None}
		]
		self.assertEquals(saves, expectedSaves)

	def test_no_argument_provided_text(self):
		self.rpg.setAction(['create-player'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_SIGNUP_NOT_ENOUGH_ARGUMENTS'))
		self.compareSavedGamesSaveKo()

	def test_no_argument_provided_json(self):
		self.rpg.setAction(['create-player'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_SIGNUP_NOT_ENOUGH_ARGUMENTS'), "code": 1}})
		self.compareSavedGamesSaveKo()

	def test_login_already_used_text(self):
		self.rpg.setAction(['create-player', 'TEST_PLAYER', 1, 1])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_SIGNUP_LOGIN_ALREADY_USED'))
		self.compareSavedGamesSaveKo()

	def test_login_already_used_json(self):
		self.rpg.setAction(['create-player', 'TEST_PLAYER', 1, 1])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_SIGNUP_LOGIN_ALREADY_USED'), "code": 1}})
		self.compareSavedGamesSaveKo()

	def test_invalid_gender_text(self):
		self.rpg.setAction(['create-player', 'TEST_PLAYER_SOME', 'some gender', 1])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_SIGNUP_INVALID_GENDER'))
		self.compareSavedGamesSaveKo()

	def test_invalid_gender_json(self):
		self.rpg.setAction(['create-player', 'TEST_PLAYER_SOME', 'some gender', 1])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_SIGNUP_INVALID_GENDER'), "code": 1}})
		self.compareSavedGamesSaveKo()

	def test_invalid_species_text(self):
		self.rpg.setAction(['create-player', 'TEST_PLAYER_SOME', '1', 'some species'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_SIGNUP_INVALID_SPECIES'))
		self.compareSavedGamesSaveKo()

	def test_invalid_species_json(self):
		self.rpg.setAction(['create-player', 'TEST_PLAYER_SOME', '1', 'some species'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, {"error": {"message": _('ERROR_SIGNUP_INVALID_SPECIES'), "code": 1}})
		self.compareSavedGamesSaveKo()

	def test_text(self):
		self.rpg.setAction(['create-player', 'TEST_PLAYER_SOME', '1', '1'])
		output = self.rpg._runAction()
		self.assertEquals(output, _('PLAYER_CREATION_CONFIRMATION'))
		self.compareSavedGamesSaveOk()

	def test_json(self):
		self.rpg.setAction(['create-player', 'TEST_PLAYER_SOME', '1', '1'])
		output = self.rpg._runAction(True)
		self.assertEquals(output, 'TEST_PLAYER_SOME')
		self.compareSavedGamesSaveOk()
