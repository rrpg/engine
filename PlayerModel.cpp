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
    sqlite3 *db;
    int rc;
    sqlite3_stmt *stmt = NULL;

    // Open the test.db file
    rc = sqlite3_open("database/rpg.sql", &db);

    if(rc){
        // failed
        return NULL;
    }

    string query = "SELECT id_player FROM player WHERE login = '" + login + "' AND password = '" + password + "'";

    rc = sqlite3_prepare(
        db,
        query.c_str(),
        query.size() + 1,
        &stmt,
        NULL
    );

    if (sqlite3_step(stmt) == SQLITE_ROW) {
        pm = new PlayerModel();
        pm->setPk(sqlite3_column_int(stmt, 0));
    }

    sqlite3_finalize( stmt );
    sqlite3_close( db );

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
