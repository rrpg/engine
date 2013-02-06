# -*- coding: utf8 -*-

from CommandAbstract import CommandAbstract
from CommandException import CommandException
from CharacterException import CharacterException
from Character import Character
from Sentence import Sentence
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
        sentence = Sentence.loadByCharacterIdAndTriggerWord(
            character.getId(), triggerWord
        )

        if len(sentence) is 0:
            print("What ?")
            return

        sentence = sentence[random.randint(0, len(sentence) - 1)]
        print(self.processSentence(
            sentence.getSentence(), self._player._model.getName()
        ))

    def processSentence(self, sentence, characterName):
        return string.replace(sentence, '%player_name%', characterName)
