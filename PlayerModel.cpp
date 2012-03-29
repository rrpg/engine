//      player.cpp
//

#include <cstdlib>
#include <iostream>
#include <map>
#include "sqlite3.h"
#include "PlayerModel.h"
#include "Utils.h"

using namespace std;


PlayerModel::PlayerModel()
{
}

PlayerModel* PlayerModel::loadByLoginAndPassword(string login, string password)
{
    PlayerModel *pm;

    string query = "\
        SELECT\
            id_player,\
            login\
        FROM\
            player\
        WHERE\
            login = '" + login + "' AND password = '" + password + "'\
    ";

    std::vector <std::string> model = Model::fetchOneRow(query);

    if (model.size() > 0) {
        pm = new PlayerModel();
        pm->_setPk(std::atoi(model[0].c_str()));
        pm->setLogin(model[1]);
    }

    return pm;
}

bool PlayerModel::save()
{
    _playerFields["date_creation"] = "2012-03-24";

    CharacterModel::setName(_playerFields["login"]);
    CharacterModel::save();
    _playerFields["id_character"] = Utils::itos(CharacterModel::getPk());

    _setPk(Model::insert("player", _playerFields));

    return true;
}

void PlayerModel::_setPk(int pk)
{
    _playerFields["id_player"] = Utils::itos(pk);
}

void PlayerModel::setLogin(std::string login)
{
    _playerFields["login"] = login;
}

void PlayerModel::setPassword(std::string password)
{
    _playerFields["password"] = password;
}

int PlayerModel::getPk()
{
    return std::atoi(_playerFields["id_character"].c_str());
}

std::string PlayerModel::getLogin()
{
    return _playerFields["login"];
}

std::string PlayerModel::getPassword()
{
    return _playerFields["password"];
}
