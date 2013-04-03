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
		return self._model.getSentence()


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

		sentences = Model.fetchAllRows(query, (triggerWord, idCharacter))

		if len(sentences) > 0:
			for index, sentence in enumerate(sentences):
				sentencesModels.append(model())
				sentencesModels[index]._setPk(
					sentences[index]['id_talk_answer'])
				sentencesModels[index].setWord(
					sentences[index]['trigger_word'])
				sentencesModels[index].setSentence(
					sentences[index]['sentence'])
				sentencesModels[index].setCondition(
					sentences[index]['condition'])

		return sentencesModels

	def setWord(self, word):
		self._sentenceFields["word"] = word

	def setSentence(self, sentence):
		self._sentenceFields["sentence"] = sentence

	def setCondition(self, condition):
		self._sentenceFields["condition"] = condition

	def _setPk(self, pk):
		self._sentenceFields["id_talk_answer"] = pk

	def getSentence(self):
		return self._sentenceFields["sentence"]
