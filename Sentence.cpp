//Sentence.cpp

#include "Sentence.h"

std::vector <Sentence*> Sentence::loadByCharacterIdAndTriggerWord(int id, std::string triggerWord)
{
    std::vector <Sentence*> sentences;

    std::vector <SentenceModel*> sm = SentenceModel::loadByCharacterIdAndTriggerWord(id, triggerWord);
    int nbSentences = sm.size();
    for (int s = 0 ; s < nbSentences ; s++) {
        sentences.push_back(new Sentence());
        sentences[s]->_model = sm[s];
    }

    return sentences;
}

std::string Sentence::getSentence()
{
    return _model->getSentence();
}
