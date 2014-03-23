# -*- coding: utf-8 -*-

from models.player import player
from core import command, command_factory, utils, config, registry
import readline
import os
import json
from core.localisation import _

RENDER_TEXT = 0
RENDER_JSON = 1

class Rpg:
	_debug = False

	def __init__(self, debug, renderMode=RENDER_TEXT):
		self._debug = debug
		self._renderMode = renderMode

	def init(self, world, login, password, action):
		if world is None:
			world = config.db

		registry.set("world", world)
		if os.path.isfile(world) is False:
			raise BaseException(_('ERROR_UNKNOWN_SELECTED_WORLD'))

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
		print(_('PLAYER_SELECTION'))
		print("  1 - " + _('CHOICE_NEW_PLAYER'))
		print("  2 - " + _('CHOICE_EXISTING_PLAYER'))
		while choice != '1' and choice != '2':
			choice = utils.read(_('CHOICE_QUESTION'))

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
					print("")
					break

				if c != "":
					self._action = self.parseTypedAction(c)
					result = self._runAction()
					print("")

				if result == command_factory.quit:
					break

	def _runAction(self):
		try:
			c = command_factory.factory.create(self._player, self._action)

			if c != command_factory.quit:
				result = c.run()
				if self._renderMode == RENDER_JSON:
					print(json.dumps(result))
				else:
					c.render(result)
				return None

			return c
		except BaseException as e:
			self.renderException(e)

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
		"""
		Method to set the autocompleter and run the prompt, from utils
		"""

		completer = command.completer(sorted(command_factory.factory.mapping.keys()))
		readline.set_completer(completer.complete)
		readline.parse_and_bind('tab: complete')
		readline.set_completer_delims('')
		return utils.read(_('COMMAND_PROMPT'))

	def renderException(self, e):
		if self._debug:
			import traceback
			print(traceback.format_exc())
		elif not isinstance(e, KeyboardInterrupt):
			print(e)
