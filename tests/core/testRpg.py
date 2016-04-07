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
	idSavedGame = 1
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
		self.assertRaises(core.exception.exception, rpgEngine.initPlayer)
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

	def test_invalid_world(self):
		rpgEngine = Rpg.Rpg()
		rpgEngine.initWorld("tests/invalidDB")
		self.assertRaises(sqlite3.OperationalError, rpgEngine.initSavedGame, self.idSavedGame)

	def test_invalid_action_format(self):
		with self.assertRaises(TypeError) as raised:
			self.rpg.setAction("Not list action")
		self.assertEquals(str(raised.exception), _('ERROR_INVALID_FORMAT_ACTION'))

	def test_invalid_action_text(self):
		self.rpg.setAction(["Unknown action"])
		output = self.rpg._runAction()
		self.assertEquals(output, _('ERROR_UNKNOWN_COMMAND'))

	def test_invalid_action_json(self):
		self.rpg.setAction(["Unknown action"])
		output = self.rpg._runAction(True)
		self.assertEquals(output,  {'error': {'message': _('ERROR_UNKNOWN_COMMAND'), 'code': 1}})
