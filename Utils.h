#ifndef DEF_UTILS
#define DEF_UTILS

#include <string>

class Utils
{
    public:
    static std::vector<std::string> explode(std::string str, char sep);
    static std::string itos(int i);
};

#endif
