# -*- coding: utf-8 -*-

"""
Module to handle the characters's genders in the game.
For the moment, only a dual genders system is done.
"""

from Model import Model


class model(Model):
	"""
	Model class to interact with the genders in the database.
	"""

	fields = ['id_gender', 'name']
