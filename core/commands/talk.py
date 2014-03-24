# -*- coding: utf-8 -*-

from models import character, sentence
import random
import core.command
from core.localisation import _

class talk(core.command.command):
	"""
	Talk command
	"""

	def run(self):
		"""
		Say something to a character in the player's area.
		"""
		if len(self._args) == 0:
			raise core.command.exception(_('ERROR_TALK_NO_CHARACTER_GIVEN'))
		elif len(self._args) == 1:
			raise core.command.exception(_('ERROR_TALK_NO_SENTENCE_GIVEN'))

		characterName = self._args[0]
		triggerWord = self._args[1]
		c = character.character.searchByNameAndIdArea(
			characterName, self._player.getAreaId()
		)

		if c is None:
			raise character.exception(_('ERROR_TALK_UNKNOWN_CHARACTER'))

		s = sentence.sentence.loadByCharacterIdAndTriggerWord(
			c.getId(), triggerWord
		)

		if len(s) is 0:
			raise sentence.exception(_('ERROR_TALK_UNKNOWN_SENTENCE'))

		s = s[random.randint(0, len(s) - 1)]
		print(self.processSentence(
			s.getSentence(), self._player._model['name']
		))

	def processSentence(self, s, characterName):
		return s % {'player_name': characterName}

	def render(self, data):
		pass
