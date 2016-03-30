# -*- coding: utf-8 -*-

import core
import core.Rpg
from core import utils
from models import player, gender, species
from core.localisation import _
from core import command, command_factory
import readline


class main:
	_debug = False

	def __init__(self, debug=False, world=''):
		self._engine = core.Rpg.Rpg(debug)

		try:
			self._engine.init(world)
			self._doInteractiveAuth()
		except (KeyboardInterrupt, EOFError):
			print("")
			return
		except BaseException as e:
			e = self._engine.renderException(e)
			if e is not None:
				print(e)
			return

		self.run()

	def _doInteractiveAuth(self): # pragma: no cover
		'''
		This method asks the player to login or to create a new account
		'''

		choice = self.choiceMenu(
			_('PLAYER_SELECTION'), _('CHOICE_QUESTION'),
			[_('CHOICE_NEW_PLAYER'), _('CHOICE_EXISTING_PLAYER')]
		)

		if choice == 0:
			(login, genderId, speciesId) = self._interactivePlayerCreation()
			self._engine.setAction(['create-player', login, genderId, speciesId])
			print(self._engine._runAction())
		elif choice == 1:
			login = self._promptLoginFromStdin()

		self._engine._initPlayer(login)

	def _interactivePlayerCreation(self): # pragma: no cover
		login = None
		while login is None or login == '':
			login = utils.read(_('LOGIN_PROMPT'))

			if len(player.model.loadBy({'login': login})):
				print(_('ERROR_SIGNUP_LOGIN_ALREADY_USED'))
				login = None

		genders = gender.model.loadAll()

		g = self.choiceMenu(
			_('GENDER_SELECTION'), _('GENDER_PROMPT'),
			[g['name'] for g in genders]
		)

		genderId = genders[g]['id_gender']

		sps = species.model.getSpecies()
		nbSpecies = len(sps)

		if nbSpecies == 1:
			speciesIndex = 0
		else:
			speciesIndex = self.choiceMenu(
				_('SPECIES_SELECTION'), _('SPECIES_PROMPT'),
				[g['name'] for g in sps]
			)

		speciesId = sps[speciesIndex]['id_species']

		return (login, genderId, speciesId)

	def _promptLoginFromStdin(self): # pragma: no cover
		'''
		Ask the player to type his login
		'''
		login = ''
		while login == '':
			login = utils.read(_('LOGIN_PROMPT'))

		return login

	def _gameOver(self): # pragma: no cover
		print(_('GAME_OVER_TEXT'))

	def run(self): # pragma: no cover
		'''
		Main method of the Rpg Class, will ask the player to enter a command
		'''
		c = ''
		result = 0
		while not self._engine.isGameOver():
			try:
				c = self.readCommand()
			except KeyboardInterrupt:
				print("")
				continue
			except EOFError:
				print("")
				break

			if c != "":
				self._engine.setAction(main.parseTypedAction(c))
				result = self._engine._runAction()

			if result == command_factory.quit:
				break
			elif c != "":
				print(result)
				print("")

		if self._engine.isGameOver():
			self._gameOver()

	@staticmethod
	def parseTypedAction(action):
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

	def choiceMenu(self, question, prompt, choices):
		print(question)
		for k, v in enumerate(choices):
			print(str(k + 1).rjust(3) + ' - ' + v)

		v = 0
		while v <= 0 or v >= len(choices) + 1:
			v = utils.read(prompt)
			try:
				v = int(v)
			except:
				v = -0

		return v - 1
