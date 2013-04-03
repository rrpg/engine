# -*- coding: utf8 -*-

from CommandAbstract import CommandAbstract
from CommandException import CommandException
from CharacterException import CharacterException
from Character import Character
from sentence import sentence
import random
import string


class CommandTalk(CommandAbstract):
	def run(self):
		if len(self._args) == 0:
			raise CommandException("Who must I talk to ?")
		elif len(self._args) == 1:
			raise CommandException("What must I say ?")

		characterName = self._args[0]
		triggerWord = self._args[1]
		character = Character.searchByNameAndPlayer(
			characterName, self._player
		)

		if character is None:
			raise CharacterException("Unknown Character")
		s = sentence.loadByCharacterIdAndTriggerWord(
			character.getId(), triggerWord
		)

		if len(s) is 0:
			print("What ?")
			return

		s = s[random.randint(0, len(s) - 1)]
		print(self.processSentence(
			s.getSentence(), self._player._model.getName()
		))

	def processSentence(self, s, characterName):
		return s % {'player_name': characterName}
