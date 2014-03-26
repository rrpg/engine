import unittest
import os
import core.config


class common(unittest.TestCase):
	def __init__(self, methodName='runTest'):
		unittest.TestCase.__init__(self, methodName)
		core.config.memoization_enabled = False

	def setUp(self):
		db = os.path.realpath(os.path.dirname(__file__) + "/../database/rpg.db")
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
