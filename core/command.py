# -*- coding: utf-8 -*-

from core.localisation import _
import core.exception


class command():
	"""
	Base class for the commands
	"""

	def __init__(self):
		pass

	def setArgs(self, args):
		"""
		c.setArgs(args)

		Define the arguments of the command.

		@params list arguments of the command to run
		"""
		self._args = args

	def setPlayer(self, p):
		"""
		c.setPlayer(p)

		Define the current player in the command's context.

		@params player.player
		"""
		self._player = p

	def setSavedGameId(self, savedGameId):
		"""
		c.setSavedGameId(savedGameId)

		Define the current savedGame id in the command's context.

		@params integer
		"""
		self._savedGameId = savedGameId


class completer:
	"""
	Class to autocomplete use choice while typing a command
	"""

	def __init__(self, commands):
		"""
		Construct. Set the available commands in an options var
		"""
		self.options = commands

	def complete(self, text, state):
		"""
		Called method when autocomplete is invoqued
		"""

		# on first trigger, build possible matches
		if state == 0:
			# cache matches (entries that start with entered text)
			if len(text.split(' ')) > 1:
				return text

			if text:
				self.matches = [s for s in self.options if s and s.startswith(text)]
			# no text entered, all matches possible
			else:
				self.matches = self.options[:]

		# return match indexed by state
		try:
			return self.matches[state]
		except IndexError as e:
			return None


class exception(core.exception.exception):
	"""
	Class for the exceptions concerning commands.
	"""
	pass
