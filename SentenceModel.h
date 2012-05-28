#ifndef DEF_SENTENCE_MODEL
#define DEF_SENTENCE_MODEL

#include "Model.h"

class SentenceModel: public Model
{
    public:
    static std::vector <SentenceModel*> loadByCharacterIdAndTriggerWord(int id, std::string triggerWord);
    void setWord(std::string word);
    void setSentence(std::string sentence);
    void setCondition(std::string condition);
    std::string getSentence();


    protected:
    std::map <std::string, std::string> _sentenceFields;
    void _setPk(int pk);
};

#endif
