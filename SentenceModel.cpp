//CharacterModel.cpp

#include <cstdlib>
#include <iostream>
#include <vector>
#include <string>
#include "SentenceModel.h"
#include "Utils.h"

std::vector <SentenceModel*> SentenceModel::loadByCharacterIdAndTriggerWord(int id, std::string triggerWord)
{
    std::vector <std::vector <std::string> > sentences;
    std::vector <SentenceModel*> sentencesModels;

    std::string query = "\
        SELECT\
            ta.id_talk_answer,\
            trigger_word,\
            sentence,\
            condition\
        FROM\
            talk_answer ta\
            INNER JOIN character_answer ca ON ca.id_talk_answer = ta.id_talk_answer\
        WHERE\
            trigger_word = '" + triggerWord + "'\
            AND id_character = " + Utils::itos(id) + "\
        ORDER BY RANDOM()\
        ";

    sentences = Model::fetchAllRows(query);

    if (sentences.size() == 0) {
        return sentencesModels;
    }
    else {
        int nbSentences = sentences.size();
        for (int i = 0 ; i < nbSentences ; i++) {
            sentencesModels.push_back(new SentenceModel());
            sentencesModels[i]->_setPk(std::atoi(sentences[i][0].c_str()));
            sentencesModels[i]->setWord(sentences[i][1]);
            sentencesModels[i]->setSentence(sentences[i][2]);
            sentencesModels[i]->setCondition(sentences[i][3]);
        }

        return sentencesModels;
    }
}

void SentenceModel::setWord(std::string word)
{
    _sentenceFields["word"] = word;
}

void SentenceModel::setSentence(std::string sentence)
{
    _sentenceFields["sentence"] = sentence;
}
void SentenceModel::setCondition(std::string condition)
{
    _sentenceFields["condition"] = condition;
}

void SentenceModel::_setPk(int pk)
{
    _sentenceFields["id_talk_answer"] = Utils::itos(pk);
}

std::string SentenceModel::getSentence()
{
    return _sentenceFields["sentence"];
}
