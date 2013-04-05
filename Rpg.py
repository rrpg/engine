# -*- coding: utf8 -*-

from player import player
from CommandFactory import CommandFactory
import Command
import utils


class Rpg:
	def __init__(self, login, password, action):
		#~ if the game is launched with login/password,
		#~ the player is directly fetched
		if login is not None and password is not None:
			self._player = player(login, password)
		elif action == []:
			#else an empty player is created
			self._player = player(None, None)
			self._doInteractiveAuth()

		self._action = action

		self._player.connect()

	#~ This method asks the player to login or to create a new account
	def _doInteractiveAuth(self):
		choice = 0
		while choice != '1' and choice != '2':
			choice = utils.read("new account (1) or login (2) ? ")

		if choice == '1':
			self._player.createNewPlayerFromStdIn()
		elif choice == '2':
			self._player.loadPlayerFromStdIn()

	#~ Main method of the Rpg Class, will run the action if it is given,
	#~ else ask the player to enter a command
	def run(self):
		if len(self._action) > 0:
			self._runAction()
		else:
			command = ''
			result = 0
			while 1:
				command = utils.read("Command: ")

				try:
					if command != "":
						self._action = command.split(' ')
						result = self._runAction()

					if result == Command.quit:
						break
				except BaseException as e:
					print(e)

	def _runAction(self):
		command = CommandFactory.create(self._player, self._action)

		if command != Command.quit:
			return command.run()

		return command
