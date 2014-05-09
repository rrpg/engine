# -*- coding: utf-8 -*-

from models.player import player
from core import command, command_factory, utils, config, registry
import readline
import getpass
import os
import json
from core.localisation import _
import core.exception

RENDER_TEXT = 0
RENDER_JSON = 1

class Rpg:
	_debug = False

	def __init__(self, debug=False, renderMode=RENDER_TEXT, isInteractive=True):
		"""
		Rpg's construct. Init the following attributes:
		- self._player
		- self._debug
		- self._renderMode
		- self._action
		- self._isInteractive

		The render mode can be or RENDER_TEXT or RENDER_JSON.
		If the flag isInteractive is set to False, the game will just execute
		the next action without entering the game loop, no command will be
		prompted to the user. This can be used for the tests or when the game is
		used as a service.
		"""
		self._player = None
		self._debug = debug
		self._renderMode = renderMode
		self._action = []
		self._isInteractive = isInteractive

	def init(self, world, login, password, action=None):
		"""
		Method to init the Rpg with a world, a player's login and password and
		and action. The action is optional, but the login and passwords can be
		None (for unauthentified actions such as createPlayer for example).

		Will raise an core.exception.exception if no login/password are provided
		and the provided action needs player.
		"""
		if world is None:
			world = config.db

		registry.set("world", world)
		if os.path.isfile(world) is False:
			raise core.exception.exception(_('ERROR_UNKNOWN_SELECTED_WORLD'))

		isConnected = self._initPlayer(login, password)

		if type(action) == list and len(action) > 0:
			if not isConnected \
				and command_factory.factory.commandNeedPlayer(action[0]):
				raise core.exception.exception(_('ERROR_NO_SELECTED_PLAYER'))
			self._action = action

	def _initPlayer(self, login, password):
		"""
		Method to init the player with a login and a password.
		If the interactive mode is active and no login/password are provided,
		the player will be prompted to login or create a new player
		"""
		self._player = player()
		if self._isInteractive and (login is None or password is None): # pragma: no cover
			(login, password) = self._doInteractiveAuth()

		if login is not None and password is not None:
			self._player.connect(login, password)
			return True

		return False

	def _doInteractiveAuth(self): # pragma: no cover
		'''
		This method asks the player to login or to create a new account
		'''
		choice = 0
		print(_('PLAYER_SELECTION'))
		print("  1 - " + _('CHOICE_NEW_PLAYER'))
		print("  2 - " + _('CHOICE_EXISTING_PLAYER'))
		while choice != 1 and choice != 2:
			try:
				choice = int(utils.read(_('CHOICE_QUESTION')))
			except ValueError:
				# If the typed value is not a valid integer
				pass

		if choice == 1:
			cmd = command_factory.factory.create(
				self._player, ['create-player'],
				isInteractive=True
			)
			return cmd.run()
		elif choice == 2:
			return self._promptLoginFromStdin()

	def _promptLoginFromStdin(self): # pragma: no cover
		'''
		Ask the player to type his login and password
		'''
		login = ''
		password = ''
		while login == '':
			login = utils.read(_('LOGIN_PROMPT'))

		while password == '':
			password = getpass.getpass(_('PASSWORD_PROMPT'))

		return (login, password)

	def setAction(self, action):
		'''
		Set the action to run
		'''
		if type(action) != list:
			raise TypeError("The action must be a list of strings")
		self._action = action

	def run(self): # pragma: no cover
		'''
		Main method of the Rpg Class, will run the action if it is given,
		else ask the player to enter a command
		'''
		if len(self._action) > 0:
			print(self._runAction())
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

				if result == command_factory.quit:
					break
				elif c != "":
					if self._renderMode == RENDER_JSON:
						result = json.dumps(result, ensure_ascii=False)
					print(result)
					print("")

	def _runAction(self):
		"""
		Method to execute when an action is set and ready to be executed.
		"""
		try:
			c = command_factory.factory.create(
				self._player,
				self._action,
				self._isInteractive
			)

			if c == command_factory.quit:
				return c

			result = c.run()
			if self._renderMode != RENDER_JSON:
				result = c.render(result)
			return result
		except core.exception.exception as e:
			return self.renderException(e)

	def parseTypedAction(self, action): # pragma: no cover
		"""
		Method to parse the action typed by the player to detect the action
		and the action's arguments
		"""
		inOption = False

		commands, sep, option, optionStart = list(), ' ', '', 0
		commandLen = len(action)
		for k,i in enumerate(action):
			# first letter of the option
			if i != ' ' and not inOption:
				# Set the start index of the option
				optionStart = k
				inOption = True
				# Set the option delimiter
				sep = i if i in ("'", '"') else ' '
			if inOption:
				# If the current char is the option delimiter, but not the
				# stat one
				if i == sep and k > optionStart:
					# The option is ended
					inOption = False
				elif i != sep:
					option += i

				# The option is complete, append it in the list
				if not inOption or k == commandLen - 1:
					commands.append(str(option))
					option = ''

		return commands

	def readCommand(self): # pragma: no cover
		"""
		Method to set the autocompleter and run the prompt, from utils
		"""

		completer = command.completer(
			sorted(command_factory.factory.mapping.keys())
		)
		readline.set_completer(completer.complete)
		readline.parse_and_bind('tab: complete')
		readline.set_completer_delims('')
		return utils.read(_('COMMAND_PROMPT'))

	def renderException(self, e):
		"""
		Method to call when an exception occurs to render it according to the
		defined render mode.
		"""
		import traceback
		if not isinstance(e, core.exception.exception):
			traceback.print_exc()
		else:
			if self._renderMode == RENDER_JSON:
				excep = {'error': {'code': e.code, 'message': str(e)}}
				if self._debug:
					excep['backtrace'] = traceback.format_exc()
				return excep
			elif self._debug:
				return traceback.format_exc()
			else:
				return str(e)