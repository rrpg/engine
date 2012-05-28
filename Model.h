#ifndef DEF_MODEL
#define DEF_MODEL

#include <map>
#include <string>
#include <vector>
#include "sqlite3.h"

class Model
{
    public:
    static std::vector <std::vector <std::string> > fetchAllRows(std::string query);
    static std::vector <std::string> fetchOneRow(std::string query);
    static std::string fetchOneField(std::string query);

    static int insert(std::string table, std::map <std::string, std::string> fields);
    static bool update(std::string table, std::map <std::string, std::string> fields, std::string where);
    static bool del(std::string table, std::string where);

    static sqlite3 *_db;

    protected:
    static bool _connect();
    static int _setStatement(std::string query, sqlite3_stmt*& stmt);
    static void _createRow(sqlite3_stmt*& stmt, std::vector <std::string>& currentRow, int& nbCols);
    static void _begin();
    static void _commit();
    static void _rollback();
};



#endif
