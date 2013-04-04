# -*- coding: utf8 -*-

from Model import Model


class sentence:
	@staticmethod
	def loadByCharacterIdAndTriggerWord(idCharacter, triggerWord):
		sentences = list()

		sentencesModels = model.loadByCharacterIdAndTriggerWord(
			idCharacter, triggerWord
		)
		for index, s in enumerate(sentencesModels):
			sentences.append(sentence())
			sentences[index]._model = s

		return sentences

	def getSentence(self):
		return self._model['sentence']


class model(Model):
	_sentenceFields = dict()

	@staticmethod
	def loadByCharacterIdAndTriggerWord(idCharacter, triggerWord):
		sentencesModels = list()

		query = "\
			SELECT\
				ta.id_talk_answer,\
				trigger_word,\
				sentence,\
				condition\
			FROM\
				talk_answer ta\
				INNER JOIN character_answer ca\
					ON ca.id_talk_answer = ta.id_talk_answer\
			WHERE\
				trigger_word = ?\
				AND id_character = ?\
			ORDER BY RANDOM()\
			"

		return Model.fetchAllRows(query, (triggerWord, idCharacter))
