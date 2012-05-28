#ifndef DEF_SENTENCE
#define DEF_SENTENCE

#include <vector>
#include <string>
#include "SentenceModel.h"

class Sentence
{
    public:
    static std::vector <Sentence*> loadByCharacterIdAndTriggerWord(int id, std::string triggerWord);
    std::string getSentence();

    protected:
    SentenceModel *_model;
};

#endif
