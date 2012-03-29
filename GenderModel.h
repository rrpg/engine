#ifndef DEF_GENDER_MODEL
#define DEF_GENDER_MODEL

#include <vector>
#include <string>

class GenderModel
{
    public:
    GenderModel();
    static std::vector <std::vector <std::string> > getGenders();
};

#endif
