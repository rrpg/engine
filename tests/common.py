# -*- coding: utf-8 -*-
import unittest
import os
import core.config
from core import Rpg


class common(unittest.TestCase):
	login = 'TEST_PLAYER'

	def setUp(self):
		self.dbFile = "/tmp/rpg.db"
		db = os.path.realpath(self.dbFile)
		if os.path.exists(db):
			os.remove(db)
		import sqlite3
		con = sqlite3.connect(db)
		f = open(os.path.realpath(os.path.dirname(__file__) + "/../database/structure.sql"),'r')
		s = f.read()
		con.executescript(s)
		f.close()

		f = open(os.path.realpath(os.path.dirname(__file__) + "/values-tests.sql"),'r')
		s = f.read()
		con.executescript(s)
		f.close()

		con.commit()
		con.close()

		core.config.memoization_enabled = False
		self.initialiseTextClient()
		self.initialiseJSONClient()

	def initialiseTextClient(self):
		self.rpgText = Rpg.Rpg(renderMode=Rpg.RENDER_TEXT, isInteractive=False)
		self.rpgText.init(self.dbFile, self.login)

	def initialiseJSONClient(self):
		self.rpgJSON = Rpg.Rpg(renderMode=Rpg.RENDER_JSON, isInteractive=False)
		self.rpgJSON.init(self.dbFile, self.login)

	def getInventory(self):
		return self.rpgJSON._player.getInventory()

	def compareInventory(self, inv):
		new = self.getInventory()
		self.assertTrue(inv == new)
