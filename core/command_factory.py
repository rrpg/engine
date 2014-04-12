# -*- coding: utf-8 -*-

"""
Module containing the available commands of the game, the factory class to
create the commands...
Today, the available commands are:
- look,
- talk,
- move,
- enter,
- exit,
- take,
- drop,
- inventory,
- help,
- quit
"""
import core.command
from core.commands import look, talk, move, enter, exit, take, drop, inventory,\
	help, createPlayer, listSpecies, listGenders
from core.localisation import _
import sys

"""
Code corresponding to the quit command
"""
quit = -1

class factory:
	"""
	Class to instanciate a command from a string.
	"""

	"""
	Available commands stored in a dict with as key, the commands and as value,
	the command class to execute.
	"""
	mapping = {
		_('LOOK_COMMAND'): 'look',
		_('TALK_COMMAND'): 'talk',
		_('MOVE_COMMAND'): 'move',
		_('ENTER_COMMAND'): 'enter',
		_('EXIT_COMMAND'): 'exit',
		_('TAKE_COMMAND'): 'take',
		_('DROP_COMMAND'): 'drop',
		_('INVENTORY_COMMAND'): 'inventory',
		_('INVENTORY_SHORT_COMMAND'): 'inventory',
		_('HELP_COMMAND'): 'help'
	}

	mapping_anonymous = {
		'create-player': 'createPlayer',
		'list-species': 'listSpecies',
		'list-genders': 'listGenders'
	}

	@staticmethod
	def create(p, commandFull, isInteractive):
		"""
		command.factory.create(p, commandFull) -> command.command

		Create the desired command.

		@param p player.player Current player.
		@param commandFull list command to run, the first element of the list
			is the command, the other elements are the command's arguments.

		@return the created command
		"""

		cmd = commandFull[0]
		del commandFull[0]

		if cmd in (_('QUIT_COMMAND'), _('QUIT_SHORT_COMMAND')):
			return quit
		elif cmd in factory.mapping.keys():
			module = sys.modules['core.commands.' + factory.mapping[cmd]]
			cmd = getattr(module, factory.mapping[cmd])(isInteractive)
		elif not p.isConnected() and cmd in factory.mapping_anonymous.keys():
			module = sys.modules['core.commands.' + factory.mapping_anonymous[cmd]]
			cmd = getattr(module, factory.mapping_anonymous[cmd])(isInteractive)
		else:
			raise core.command.exception(_('ERROR_UNKNOWN_COMMAND'))

		cmd.setArgs(commandFull)
		cmd.setPlayer(p)
		return cmd

	@staticmethod
	def commandNeedPlayer(cmd):
		if cmd in factory.mapping.keys():
			return True
		elif cmd in factory.mapping_anonymous.keys():
			return False
		else:
			raise core.command.exception(_('ERROR_UNKNOWN_COMMAND'))

