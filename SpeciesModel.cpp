//species model class

#include <vector>
#include <string>
#include "Model.h"
#include "SpeciesModel.h"

std::vector< std::vector<std::string> > SpeciesModel::getSpecies(std::string gender)
{
    std::string query = "\
        SELECT\
            id_species,\
            ";
    if (gender.compare("male") == 0) {
        query += "name_m,";
    }
    else {
        query += "name_f,";
    }

    query += "\
            description\
        FROM\
            species";

    return  Model::fetchAllRow(query);
}
