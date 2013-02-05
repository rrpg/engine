# -*- coding: utf8 -*-

from SentenceModel import SentenceModel

class Sentence:
    @staticmethod
    def loadByCharacterIdAndTriggerWord(idCharacter, triggerWord):
        sentences = list()

        sentencesModels = SentenceModel.loadByCharacterIdAndTriggerWord(idCharacter, triggerWord)
        for index, sentence in enumerate(sentencesModels):
            sentences.append(Sentence())
            sentences[index]._model = sentence

        return sentences

    def getSentence(self):
        return self._model.getSentence()
