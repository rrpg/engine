//Character.cpp

#include <string>
#include <iostream>
#include "Character.h"

Character::Character()
{

}

Character* Character::searchByNameAndPlayer(std::string characterName, Player* &player)
{
    Character* character = new Character();

    character->_model = CharacterModel::loadByNameAndIdPlayer(characterName, player->getModel()->getPk());

    if (character->_model != NULL) {
        return character;
    }
    else {
        return NULL;
    }
}

std::string Character::getName()
{
    return _model->getName();
}

int Character::getId()
{
    return _model->getPk();
}
