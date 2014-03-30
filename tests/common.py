# -*- coding: utf-8 -*-
import unittest
import os
import core.config
from core import Rpg


class common(unittest.TestCase):
	def __init__(self, methodName='runTest'):
		unittest.TestCase.__init__(self, methodName)
		core.config.memoization_enabled = False
		self.rpgText = Rpg.Rpg(renderMode=Rpg.RENDER_TEXT)
		self.rpgJSON = Rpg.Rpg(renderMode=Rpg.RENDER_JSON)
		self.dbFile = "/tmp/rpg.db"

	def setUp(self):
		db = os.path.realpath(self.dbFile)
		if os.path.exists(db):
			os.remove(db)
		import sqlite3
		con = sqlite3.connect(db)
		f = open(os.path.realpath(os.path.dirname(__file__) + "/../database/structure.sql"),'r')
		s = f.read()
		con.executescript(s)
		f.close()

		f = open(os.path.realpath(os.path.dirname(__file__) + "/../database/values.sql"),'r')
		s = f.read()
		con.executescript(s)
		f.close()

		con.commit()
		con.close()
