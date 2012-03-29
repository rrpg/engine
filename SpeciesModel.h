#ifndef DEF_SPECIES_MODEL
#define DEF_SPECIES_MODEL

#include <vector>
#include <string>

class SpeciesModel
{
    public:
    SpeciesModel();
    static std::vector< std::vector<std::string> > getSpecies(std::string gender);
};

#endif
