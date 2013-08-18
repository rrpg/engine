# -*- coding: utf8 -*-

from player import player
import command
import utils
import readline


class Rpg:
	_debug = False

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

	def setDebug(self, debug):
		self._debug = debug

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
			c = ''
			result = 0
			while 1:
				try:
					c = self.readCommand()
				except KeyboardInterrupt:
					print("")
					continue
				except EOFError:
					break

				if c != "":
					self._action = self.parseTypedAction(c)
					result = self._runAction()

				if result == command.quit:
					break

	def _runAction(self):
		try:
			c = command.factory.create(self._player, self._action)

			if c != command.quit:
				return c.run()

			return c
		except BaseException as e:
			if self._debug:
				import traceback
				print(traceback.format_exc())
			elif not isinstance(e,  KeyboardInterrupt):
				print(e)



	def parseTypedAction(self, action):
		inOption = False

		commands, sep, option, optionStart = list(), ' ', '', 0
		commandLen = len(action)
		for k,i in enumerate(action):
			# first letter of the option
			if i != ' ' and not inOption:
				#~ Set the start index of the option
				optionStart = k
				inOption = True
				#~ Set the option delimiter
				sep = i if i in ("'", '"') else ' '
			if inOption:
				#~ If the current char is the option delimiter, but not the
				#~ stat one
				if i == sep and k > optionStart:
					#~ The option is ended
					inOption = False
				elif i != sep:
					option += i

				#~ The option is complete, append it in the list
				if not inOption or k == commandLen - 1:
					commands.append(option)
					option = ''

		return commands

	def readCommand(self):
		completer = command.completer()
		readline.set_completer(completer.complete)
		readline.parse_and_bind('tab: complete')
		readline.set_completer_delims('')
		return utils.read("Command: ")
