# -*- coding: utf8 -*-

import Command
from CommandTalk import CommandTalk
from CommandHelp import CommandHelp
from CommandMove import CommandMove
from CommandLook import CommandLook
from CommandException import CommandException
import player


class CommandFactory:

	@staticmethod
	def create(p, commandFull):
		cmd = commandFull[0]
		del commandFull[0]

		if cmd in ("talk", "move")\
			and (not p.isConnected() or not p.connect()):
			raise player.exception(
				"A player must be connected to launch the command %s" % cmd
			)

		if cmd == "look":
			command = CommandLook()
		elif cmd == "talk":
			command = CommandTalk()
		elif cmd == "move":
			command = CommandMove()
		elif cmd == "createPlayer":
			if p.isConnected():
				raise player.exception(
					"You cannot create a new player when you're connected"
				)
		elif cmd in ('quit', 'exit', 'q'):
			return Command.quit
		elif cmd == 'help':
			command = CommandHelp()
		else:
			raise CommandException('Unknown command')

		command.setArgs(commandFull)
		command.setPlayer(p)
		return command
