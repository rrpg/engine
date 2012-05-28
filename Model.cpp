// Model.cpp

#include <iostream>
#include <map>
#include <string>
#include <vector>
#include "Model.h"
#include "sqlite3.h"


sqlite3 *Model::_db;

std::vector <std::vector <std::string> > Model::fetchAllRows(std::string query)
{
    sqlite3_stmt* stmt = NULL;
    int rc =  Model::_setStatement(query, stmt);

    std::vector <std::vector <std::string> > result;

    if (rc == SQLITE_OK) {
        std::vector <std::string> currentRow;
        int nbCols = 0;
        while (sqlite3_step(stmt) == SQLITE_ROW) {
            Model::_createRow(stmt, currentRow, nbCols);
            result.push_back(currentRow);
            currentRow.clear();
        }
    }

    return result;
}

std::vector <std::string> Model::fetchOneRow(std::string query)
{
    sqlite3_stmt* stmt = NULL;
    int rc =  Model::_setStatement(query, stmt);

    std::vector <std::string> result;

    if (rc == SQLITE_OK) {
        int nbCols = 0;
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            Model::_createRow(stmt, result, nbCols);
        }
    }

    return result;
}

std::string Model::fetchOneField(std::string query)
{
    sqlite3_stmt* stmt = NULL;
    int rc =  Model::_setStatement(query, stmt);

    if (rc == SQLITE_OK && sqlite3_step(stmt) == SQLITE_ROW) {
        return (char*) sqlite3_column_text(stmt, 0);
    }

    return NULL;
}



int Model::insert(std::string table, std::map <std::string, std::string> fields)
{
    if (!Model::_connect()) {
        throw "Can't connect to the DB";
    }

    std::string query = "INSERT INTO " + table;
    std::string fieldsStr, valuesStr;

    int nbFields = fields.size();
    int current = 0;
    for ( std::map< std::string, std::string >::const_iterator iter = fields.begin(); iter != fields.end(); iter++ ) {
        fieldsStr = fieldsStr + '"' + iter->first + '"' + (current < nbFields - 1 ? ", " : "");
        valuesStr = valuesStr + '"' + iter->second + '"' + (current < nbFields - 1 ? ", " : "");
        current++;
    }

    query = query + " (" + fieldsStr + ") VALUES (" + valuesStr + ")";

    int rc;
    Model::_begin();
    rc = sqlite3_exec(
        Model::_db,
        query.c_str(),
        0,
        NULL,
        NULL
    );

    if (rc != SQLITE_OK) {
        std::cout << query << std::endl;
        Model::_rollback();
        throw rc;
    }

    rc = (int) sqlite3_last_insert_rowid (Model::_db);
    Model::_commit();

    return rc;
}

bool Model::update(std::string table, std::map <std::string, std::string> fields, std::string where)
{
    return 1;
}

bool Model::del(std::string table, std::string where)
{
    return 1;
}

bool Model::_connect()
{
    int rc;

    if (Model::_db == NULL) {
        //@TODO move in conf
        rc = sqlite3_open("database/rpg.db", &Model::_db);

        if (rc != SQLITE_OK) {
            return false;
        }
    }

    return true;
}

int Model::_setStatement(std::string query, sqlite3_stmt*& stmt)
{
    if (!Model::_connect()) {
        throw "Can't connect to the DB";
    }

    int rc;
    rc = sqlite3_prepare(
        Model::_db,
        query.c_str(),
        query.size() + 1,
        &stmt,
        NULL
    );

    return rc;
}

void Model::_createRow(sqlite3_stmt*& stmt, std::vector <std::string> &currentRow, int& nbCols)
{
    if (nbCols == 0) {
        nbCols = sqlite3_column_count(stmt);
    }
    for (int i = 0 ; i < nbCols ; i++) {
        currentRow.push_back((char*) sqlite3_column_text(stmt, i));
    }
}

void Model::_begin()
{
    sqlite3_exec(Model::_db, "BEGIN", 0, 0, 0);
}

void Model::_commit()
{
    sqlite3_exec(Model::_db, "COMMIT", 0, 0, 0);
}

void Model::_rollback()
{
    sqlite3_exec(Model::_db, "ROLLBACK", 0, 0, 0);
}
