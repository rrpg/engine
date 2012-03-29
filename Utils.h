#ifndef DEF_UTILS
#define DEF_UTILS

#include <vector>
#include <string>

class Utils
{
    public:
    static std::vector<std::string> explode(std::string str, char sep);
    static bool in_array(const std::string &needle, const std::vector< std::string > &haystack);
    static std::string itos(int i);
};

#endif
