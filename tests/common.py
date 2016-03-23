# -*- coding: utf-8 -*-
from __future__ import absolute_import
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

		self.initialiseTextClient()
		self.initialiseJSONClient()

	def initialiseTextClient(self):
		self.rpgText = Rpg.Rpg(renderMode=Rpg.RENDER_TEXT)
		self.rpgText.init(self.dbFile, self.login)

	def initialiseJSONClient(self):
		self.rpgJSON = Rpg.Rpg(renderMode=Rpg.RENDER_JSON)
		self.rpgJSON.init(self.dbFile, self.login)

	def getInventory(self):
		return self.rpgJSON._player.getInventory()

	def compareInventory(self, inv):
		new = self.getInventory()
		self.assertTrue(inv == new)
