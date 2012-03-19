//      player.cpp
//

#include <iostream>
#include <string>
#include "sqlite3.h"
#include "PlayerModel.h"

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
        //~ pm->setPk(sqlite3_column_int(stmt, 0));
        pm->_pk = sqlite3_column_int(stmt, 0);
    }

    sqlite3_finalize( stmt );
    sqlite3_close( db );

    return pm;
}

//~ void setPk(int pk)
//~ {
    //~ _pk = pk;
//~ }
