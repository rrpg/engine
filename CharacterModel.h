#ifndef DEF_CHARACTER_MODEL
#define DEF_CHARACTER_MODEL

#include "Model.h"

class CharacterModel: public Model
{
    public:
    void setSpecies(int species);
    void setGender(int gender);
    void setName(std::string name);
    std::string getName();
    int getPk();
    bool save();
    static CharacterModel* loadByNameAndIdPlayer(std::string name, int playerId);

    protected:
    std::map <std::string, std::string> _characterFields;
    void _setPk(int pk);
};

#endif
