# -*- coding: utf-8 -*-
import unittest

import tests.common
import core
from core.localisation import _
from core import Rpg
import models.player
from models.saved_game import saved_game

import json
import sqlite3


class rpgTests(tests.common.common):
	idSavedGame = 1
	idFaultySavedGame = 2
	idEmptySavedGame = 3
	incorrectIdSavedGame = 42

	def test_unknown_world(self):
		rpgEngine = Rpg.Rpg()
		try:
			rpgEngine.initWorld("some/unexisting/world")
		except core.exception.exception as e:
			self.assertEquals(str(e), _('ERROR_UNKNOWN_SELECTED_WORLD'))

	def test_invalid_saved_game_id(self):
		rpgEngine = Rpg.Rpg()
		rpgEngine.initWorld(self.dbFile)
		with self.assertRaises(core.exception.exception) as raised:
			rpgEngine.initSavedGame(self.incorrectIdSavedGame)
		self.assertEquals(str(raised.exception), _('ERROR_RRPG_INIT_INVALID_SAVED_GAME_ID'))

	def test_load_player_with_no_save(self):
		rpgEngine = Rpg.Rpg()
		rpgEngine.initWorld(self.dbFile)
		with self.assertRaises(core.exception.exception) as raised:
			rpgEngine.initPlayer()
		self.assertEquals(str(raised.exception), _('ERROR_SAVED_GAME_NEEDED_TO_INIT_PLAYER'))

	def test_load_player_with_empty_save(self):
		rpgEngine = Rpg.Rpg()
		rpgEngine.initWorld(self.dbFile)
		rpgEngine.initSavedGame(self.idEmptySavedGame)
		with self.assertRaises(core.exception.exception) as raised:
			rpgEngine.initPlayer()
		self.assertEquals(str(raised.exception), _('ERROR_NON_EMPTY_SAVED_GAME_NEEDED_TO_INIT_PLAYER'))

	def test_load_player_with_faulty_save(self):
		rpgEngine = Rpg.Rpg()
		rpgEngine.initWorld(self.dbFile)
		rpgEngine.initSavedGame(self.idFaultySavedGame)
		with self.assertRaises(core.exception.exception) as raised:
			rpgEngine.initPlayer()
		self.assertEquals(str(raised.exception), _('ERROR_CONNECT_INVALID_CREDENTIALS'))

	def test_invalid_world(self):
		rpgEngine = Rpg.Rpg()
		rpgEngine.initWorld("tests/invalidDB")
		rpgEngine.initSavedGame(self.idSavedGame)
		self.assertRaises(sqlite3.OperationalError, rpgEngine.initPlayer)

	def test_invalid_action_format(self):
		with self.assertRaises(TypeError) as raised:
			self.rpg.setAction("Not list action")
		self.assertEquals(str(raised.exception), _('ERROR_INVALID_FORMAT_ACTION'))

	def test_invalid_action_text(self):
		self.rpg.setAction(["Unknown action"])
		output = self.rpg._runAction()
		self.assertEquals(output,  _('ERROR_UNKNOWN_COMMAND'))

	def test_invalid_action_json(self):
		self.rpg.setAction(["Unknown action"])
		output = self.rpg._runAction(True)
		self.assertEquals(output,  {'error': {'message': _('ERROR_UNKNOWN_COMMAND'), 'code': 1}})

	def compareSavedGamesSaveOk(self):
		saves = saved_game.loadAll()
		expectedSaves = [
			{
				'id_saved_game': 1,
				'snapshot_player': '{"id_gender": 1, "name": "TEST_PLAYER_SOME", "id_character": 4, "id_player": 3, "stat_defence": 2, "stat_attack": 4, "stat_max_hp": 20, "inventory": null, "id_area": 1, "stat_current_hp": 20, "login": "TEST_PLAYER_SOME", "stat_speed": 2, "id_species": 1, "stat_luck": 10}',
				'id_player': 3,
				'id_character': 4
			},
			{
				'id_saved_game': 2,
				'snapshot_player': '{"id_gender": 1, "name": "TEST_PLAYER2bis", "id_character": 3, "id_player": 2, "stat_defence": 2, "stat_attack": 4, "stat_max_hp": 20, "inventory": null, "id_area": 1, "stat_current_hp": 20, "login": "TEST_PLAYER2bis", "stat_speed": 2, "id_species": 1, "stat_luck": 10}',
				'id_player': 2,
				'id_character': 3
			},
			{
				'id_saved_game': 3,
				'snapshot_player': '',
				'id_player': None,
				'id_character': None
			}
		]
		self.assertEquals(saves, expectedSaves)

	def compareSavedGamesSaveKo(self):
		saves = saved_game.loadAll()
		expectedSaves = [
			{
				'id_saved_game': 1,
				'snapshot_player': '{"id_gender": 1, "name": "TEST_PLAYER", "id_character": 2, "id_player": 1, "stat_defence": 2, "stat_attack": 4, "stat_max_hp": 20, "inventory": null, "id_area": 1, "stat_current_hp": 20, "login": "TEST_PLAYER", "stat_speed": 2, "id_species": 1, "stat_luck": 10}',
				'id_player': 1,
				'id_character': 2
			},
			{
				'id_saved_game': 2,
				'snapshot_player': '{"id_gender": 1, "name": "TEST_PLAYER2bis", "id_character": 3, "id_player": 2, "stat_defence": 2, "stat_attack": 4, "stat_max_hp": 20, "inventory": null, "id_area": 1, "stat_current_hp": 20, "login": "TEST_PLAYER2bis", "stat_speed": 2, "id_species": 1, "stat_luck": 10}',
				'id_player': 2,
				'id_character': 3
			},
			{
				'id_saved_game': 3,
				'snapshot_player': '',
				'id_player': None,
				'id_character': None
			}
		]
		self.assertEquals(saves, expectedSaves)

	def test_login_already_used(self):
		with self.assertRaises(models.player.exception) as raised:
			self.rpg.createPlayer('TEST_PLAYER', 1, 1)
		self.assertEquals(str(raised.exception), _('ERROR_SIGNUP_LOGIN_ALREADY_USED'))
		self.compareSavedGamesSaveKo()

	def test_invalid_gender(self):
		with self.assertRaises(models.player.exception) as raised:
			self.rpg.createPlayer('TEST_PLAYER_SOME', 'some gender', 1)
		self.assertEquals(str(raised.exception), _('ERROR_SIGNUP_INVALID_GENDER'))
		self.compareSavedGamesSaveKo()

	def test_invalid_species(self):
		with self.assertRaises(models.player.exception) as raised:
			self.rpg.createPlayer('TEST_PLAYER_SOME', 1, 'some species')
		self.assertEquals(str(raised.exception), _('ERROR_SIGNUP_INVALID_SPECIES'))
		self.compareSavedGamesSaveKo()

	def test_ok(self):
		self.rpg.createPlayer('TEST_PLAYER_SOME', '1', '1')
		self.compareSavedGamesSaveOk()

	def test_command_with_no_saved_game(self):
		rpgEngine = Rpg.Rpg()
		rpgEngine.setAction([_('LOOK_COMMAND')])
		with self.assertRaises(core.exception.exception) as raised:
			rpgEngine._runAction(True)
		self.assertEquals(str(raised.exception), _('ERROR_SAVED_GAME_NEEDED_TO_RUN_ACTION'))

	def test_command_with_no_player(self):
		rpgEngine = Rpg.Rpg()
		rpgEngine.initWorld(self.dbFile)
		rpgEngine.initSavedGame(self.idEmptySavedGame)
		rpgEngine.setAction([_('LOOK_COMMAND')])
		with self.assertRaises(core.exception.exception) as raised:
			rpgEngine._runAction(True)
		self.assertEquals(str(raised.exception), _('ERROR_CONNECTED_PLAYER_NEEDED_FOR_COMMAND'))

	def test_run_action_with_no_action(self):
		with self.assertRaises(core.exception.exception) as raised:
			self.rpg._runAction()
		self.assertEquals(str(raised.exception), _('ERROR_NO_ACTION_SET'))
