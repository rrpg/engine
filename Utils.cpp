// Utils.cpp

#include <iostream>
#include <string>
#include <vector>
#include "Utils.h"


std::vector<std::string> Utils::explode(std::string str, char sep)
{
    std::vector<std::string> retValue;
    int sizeStr = str.size();
    unsigned int start = 0, length = 0;
    for (int i = 0 ; i < sizeStr ; i++) {
        if (str[i] == sep) {
            retValue.push_back(str.substr(start, length));
            start = i + 1;
            length = 0;
        }
        length++;
    }

    if (start < str.size()) {
        retValue.push_back(str.substr(start, length));
    }

    return retValue;
}
