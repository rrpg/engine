# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest
import os
import sqlite3

import core.config
from core import Rpg


class common(unittest.TestCase):
	initPlayer = True

	def setUp(self):
		self.dbFile = "/tmp/rpg.db"
		db = os.path.realpath(self.dbFile)
		if os.path.exists(db):
			os.remove(db)

		con = sqlite3.connect(db)
		f = open(os.path.realpath(os.path.dirname(__file__) + "/../database/structure.sql"),'r')
		s = f.read()
		con.executescript(s)
		f.close()

		f = open(os.path.realpath(os.path.dirname(__file__) + "/values-tests.sql"),'r')
		s = f.read()
		con.executescript(s)
		f.close()

		core.config.nexusDb = '/tmp/nexus-rrpg.db'
		dbNexus = os.path.realpath(core.config.nexusDb)
		if os.path.exists(dbNexus):
			os.remove(dbNexus)

		conNexus = sqlite3.connect(dbNexus)
		f = open(os.path.realpath(os.path.dirname(__file__) + "/../database/nexus.sql"),'r')
		s = f.read()
		conNexus.executescript(s)
		f.close()

		f = open(os.path.realpath(os.path.dirname(__file__) + "/values-nexus-tests.sql"),'r')
		s = f.read()
		conNexus.executescript(s)
		f.close()

		conNexus.commit()
		conNexus.close()

		self.initialiseClient()

	def initialiseClient(self, initPlayer=True):
		self.rpg = Rpg.Rpg()
		self.rpg.initWorld(self.dbFile)
		self.rpg.initSavedGame(1)

		if self.initPlayer:
			self.rpg.initPlayer()

	def getInventory(self):
		return self.rpg._player.getInventory()

	def compareInventory(self, inv):
		new = self.getInventory()
		self.assertTrue(inv == new)
