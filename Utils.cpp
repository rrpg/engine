// Utils.cpp

#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include "Utils.h"


std::vector<std::string> Utils::explode(std::string str, char sep)
{
    std::vector<std::string> retValue;
    int sizeStr = str.size();
    unsigned int start = 0, length = 0;
    for (int i = 0 ; i < sizeStr ; i++) {
        if (str[i] != sep) {
            length++;
        }
        else {
            retValue.push_back(str.substr(start, length));
            start = i + 1;
            length = 0;
        }
    }

    if (start < str.size()) {
        retValue.push_back(str.substr(start, length));
    }

    return retValue;
}

bool Utils::in_array(const std::string &needle, const std::vector< std::string > &haystack)
{
    int max = haystack.size();

    if (max==0) {
        return false;
    }

    for (int i = 0 ; i < max ; i++) {
        if (haystack[i] == needle) {
            return true;
        }
    }

    return false;
}

std::string Utils::itos(int i)
{
    std::ostringstream out;
    out << i;
    return out.str();
}


std::string Utils::ltrim(std::string str, char c)
{
    size_t lastSpace = str.find_first_not_of(c);

    if (lastSpace == std::string::npos) {
        return str;
    }

    return str.substr(lastSpace + 1, str.size() - lastSpace + 1);
}

std::string Utils::rtrim(std::string str, char c)
{
    size_t firstSpace = str.find_last_not_of(c);

    if (firstSpace == std::string::npos) {
        return str;
    }

    return str.substr(0, firstSpace - 1);
}

std::string Utils::trim(std::string str, char c)
{
    return Utils::rtrim(Utils::ltrim(str, c), c);
}
