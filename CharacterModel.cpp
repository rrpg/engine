//CharacterModel.cpp

#include <cstdlib>
#include <iostream>
#include <string>
#include "CharacterModel.h"
#include "Utils.h"
#include "PlayerModel.h"

void CharacterModel::setSpecies(int species)
{
    _characterFields["id_species"] = Utils::itos(species);
}

void CharacterModel::setGender(int gender)
{
    _characterFields["id_gender"] = Utils::itos(gender);
}

void CharacterModel::setName(std::string name)
{
    _characterFields["name"] = name;
}

void CharacterModel::_setPk(int pk)
{
    _characterFields["id_character"] = Utils::itos(pk);
}

int CharacterModel::getPk()
{
    return std::atoi(_characterFields["id_character"].c_str());
}

std::string CharacterModel::getName()
{
    return _characterFields["name"];
}

bool CharacterModel::save()
{
    _setPk(Model::insert("character", _characterFields));

    return true;
}

CharacterModel* CharacterModel::loadByNameAndIdPlayer(std::string name, int playerId)
{
    std::vector <std::string> character;

    std::string query = "\
        SELECT\
            id_character,\
            name,\
            id_species,\
            id_gender\
        FROM\
            `character`\
        WHERE\
            name = '" + name + "'\
        LIMIT 1";

    character = Model::fetchOneRow(query);

    if (character.size() == 0) {
        return NULL;
    }
    else {
        CharacterModel* model = new CharacterModel();
        model->_setPk(std::atoi(character[0].c_str()));
        model->setName(character[1]);
        model->setSpecies(std::atoi(character[2].c_str()));
        model->setGender(std::atoi(character[3].c_str()));

        return model;
    }
}
