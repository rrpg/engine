#ifndef DEF_CHARACTER
#define DEF_CHARACTER

#include <string>
#include "Player.h"

class Character
{
    public:
    Character();
    static Character* searchByNameAndPlayer(std::string characterName, Player* &_player);
    std::string getName();
    int getId();

    protected:
    CharacterModel *_model;
};

#endif
