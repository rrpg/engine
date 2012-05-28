//gender model class

#include <vector>
#include <string>
#include "GenderModel.h"
#include "Model.h"

std::vector <std::vector <std::string> > GenderModel::getGenders()
{
    std::vector <std::vector <std::string> > genders;

    std::string query = "\
        SELECT\
            id_gender,\
            name\
        FROM\
            gender\
    ";

    genders = Model::fetchAllRows(query);

    return genders;
}
